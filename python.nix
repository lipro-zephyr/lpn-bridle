{ python3
, zephyr
, bridle
, python-deps
, pyproject-nix
, clang-tools
, gitlint
, lib
}:

let

  # Create a python whose `withPackages` knows about some extra stuff we need
  python = python3.override {
    self = python;
    packageOverrides = final: prev: {
      # HACK: Zephyr uses pypi to install non-Python deps
      clang-format = clang-tools;
      inherit gitlint;

      # Extra python packages that aren't in nixpkgs
      inherit (python-deps)
        doxmlparser
        pydebuggerconfig
        pyedbglib
        pykitinfo
        pymcuprog
        sphinx-tsn-theme
        sphinxcontrib-svg2pdfconverter
        sphinx-csv-filter;
    };
  };

  # Parse requirements.txt files into pyproject-nix projects
  zephyr-project = pyproject-nix.lib.project.loadRequirementsTxt {
    requirements = zephyr + "/scripts/requirements.txt";
  };

  bridle-project = pyproject-nix.lib.project.loadRequirementsTxt {
    requirements = bridle + "/scripts/requirements.txt";
  };

  # Can't validate the combined packages sets, but we can at least check for
  # conflicts within each subset
  invalidConstraints = zephyr-project.validators.validateVersionConstraints { inherit python; }
    // bridle-project.validators.validateVersionConstraints { inherit python; };

in
lib.warnIf
  (invalidConstraints != { })
  "pythonEnv: Found invalid Python constraints for: ${builtins.toJSON (lib.attrNames invalidConstraints)}"
  (python.buildEnv.override {
    extraLibs = (bridle-project.renderers.withPackages {
      inherit python;
      # Nest one project's withPackages within the other to get a combined package
      # set. If we want more than two, we should name these lambdas to reduce
      # indentation.
      extraPackages = (zephyr-project.renderers.withPackages {
        inherit python;
        extraPackages = ps: [ ps.west ];
      });
    }) python.pkgs;
    ignoreCollisions = true;
  })
