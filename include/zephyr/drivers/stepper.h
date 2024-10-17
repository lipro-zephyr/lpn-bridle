/*
 * SPDX-FileCopyrightText: Copyright (c) 2024 Carl Zeiss Meditec AG
 * SPDX-FileCopyrightText: Copyright (c) 2024 TiaC Systems
 *
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @file
 * @brief Public Stepper Motor API
 */

#ifndef ZEPHYR_INCLUDE_DRIVERS_STEPPER_H_
#define ZEPHYR_INCLUDE_DRIVERS_STEPPER_H_

#include <errno.h>
#include <stdlib.h>
#include <string.h>
#include <zephyr/device.h>
#include <zephyr/devicetree/motors.h>
#include <zephyr/dt-bindings/stepper/stepper.h>
#include <zephyr/kernel.h>
#include <zephyr/sys/__assert.h>
#include <zephyr/sys/atomic.h>
#include <zephyr/sys/iterable_sections.h>
#include <zephyr/types.h>

#include "zephyr/devicetree.h"
#include "zephyr/sys/util.h"

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Stepper Motor Interface
 * @defgroup stepper_interface Stepper Motor Interface
 * @since 4.0
 * @version 0.1.0
 * @ingroup io_interfaces
 * @{
 *
 * @details Stepper motors are manufactured with two coils of wire, resulting
 * in one winding per phase. By alternating the power between coils, as well
 * as the direction of the current, the motor is rotated. The stepper motor
 * can reverse the direction of rotation simply by reversing this sequence.
 * The wiring of the two phases, or more precisely the start and end of the
 * two coils, to the stepper motor driver determines the default direction of
 * rotation. Mostly this is "forward" or "right" direction for "positive" and
 * "backward" or "left" direction for "negative".
 *
 * Depending on the number of these sequential individual steps and the amount
 * with which they occur in relation to time, a stepper motor can be operated
 * either for precise positioning in the "positioning mode" or highly constant
 * rotational speed in the "velocity mode", also often called "free running":
 *
 * - @see STEPPER_OP_MODE_POSITION for "positioning mode"
 * - @see STEPPER_OP_MODE_VELOCITY for "velocity mode" (free running)
 *
 * The final direction of rotation is determined by a "positive" or "negative"
 * value. In the case of "positioning mode" by "microsteps" as the position and
 * in "velocity mode" by the "rotational speed" as the velocity.
 *
 * The terms "position" and "microsteps" are ambivalent, unitless and often
 * have the same meaning, depending on the context in which they are used. In
 * "positioning mode", the value of the microsteps can be designated only as
 * "relative". Relative microsteps move the stepper motor away from the current
 * (stepper motor owned) absolute position accordingly.
 *
 * In "velocity mode", the value of velocity, the rotational speed, is defined
 * as "microsteps per second" and can be designated only as "absolute".
 * Absolute velocity, in other words a "new velocity", change the rotational
 * speed exactly.
 *
 * @note In "velocity mode", the value of velocity is defined as "microsteps
 * per second" based to "full-stepping" (internal multiplicated by current
 * microstep resolution). Common values are:
 *
 * -   < 10 (extremely slow),
 * -    100 (very slow),
 * -    500 (fast),
 * -   1000 (very fast),
 * - > 1500 (extremely fast).
 *
 * These are only example values for full steps, where the resolution of
 * microsteps is defined as 1 (no multiplications). Depending on the common
 * step angles, usage of microstep resolution greater than 1 and whether
 * gears also play a role, these values can be completely different.
 *
 * @note When a stepper motor becomes engaged in software, and current is
 * applied to the coils, it may abruptly "snap" to the position that the
 * rotor is being held at.
 *
 */

/**
 * @name Stepper motor operation mode flags used to specify driver capabilities.
 * @{
 *
 */

/** Enable positioning mode (forward or backward) by microsteps. */
#define STEPPER_OP_MODE_POSITION (1U << 16)

/** Enable free running mode (forward or backward) by velocity. */
#define STEPPER_OP_MODE_VELOCITY (1U << 17)

/** Enable accelerating mode (forward or backward) by acceleration. */
#define STEPPER_OP_MODE_ACCELERATION (1U << 18)

/** Enable smooth position mode (forward or backward) by microsteps. */
#define STEPPER_OP_MODE_POSITION_SMOOTH (1U << 19)

/** @} */

/**
 * @brief Types of stepper actions.
 *
 * @note Uses the bit-field constants defined above to make comparisons against
 * driver capability flags easier.
 */
enum stepper_action_type {
	/** Moving the motor by a precise amount of steps. */
	STEPPER_ACTION_TYPE_POSIIONING = STEPPER_OP_MODE_POSITION,
	/** Moving the motor at a constant rate for a specified time. */
	STEPPER_ACTION_TYPE_VELOCITY = STEPPER_OP_MODE_VELOCITY,
	/** Moving the motor with a constant acceleration. */
	STEPPER_ACTION_TYPE_ACCELERATION = STEPPER_OP_MODE_ACCELERATION,
	/** Moving the motor by a precise number of steps with smooth acceleration and deceleration.
	 */
	STEPPER_ACTION_TYPE_POSITIONING_SMOOTH = STEPPER_OP_MODE_POSITION_SMOOTH,
};

/**
 * @brief Representation of a stepper action.
 *
 * @details The action structure represents all values that are
 * required for general or special actions that can be executed by stepper
 * motors.
 */
struct stepper_action {
	/** Type of this action. */
	enum stepper_action_type type;
	/** Additional flags, e.g. microstep resolution. */
	uint32_t flags;
	union {
		/** Step-precise movement with constant velocity. */
		struct positioning_action {
			/** Stepping velocity during this movement
			 * (full-steps/s). Sign encodes direction.
			 */
			int32_t velocity;
			/** Number of steps to take */
			uint32_t steps;
		} positioning;
		/** Coasting at constant velocity for specified time */
		struct velocity_action {
			/** Stepping velocity (full-steps/s) (sign encodes
			 * direction).
			 */
			int32_t velocity;
			/** Coasting time in microseconds. */
			uint32_t duration_us;
		} velocity;
		struct acceleration_action {
			/** Stepping velocity at the start of the action
			 * (full-steps/s). */
			int32_t start_velocity;
			/** Stepping velocity at the end of the action
			 * (full-steps/s). */
			int32_t end_velocity;
			/** Duration of the action in microseconds */
			uint32_t duration_us;
		} acceleration;
		struct positioning_smooth_action {
			/** TODO: Resolve inconsistency with positioning action */
			/** Number of steps to take (sign encodes direction) */
			int32_t steps;
			/** Maximum stepping rate (full-steps/s). */
			uint32_t max_velocity;
			/** Time in which maximum stepping rate may be reached (microseconds). */
			uint32_t acceleration_time_us;
		} positioning_smooth;
	} action;
};

#define STEPPER_ACTION_STOP                                                                        \
	(struct stepper_action)                                                                    \
	{                                                                                          \
		.type = STEPPER_ACTION_TYPE_VELOCITY, .flags = STEPPER_USTEP_RES_1,                \
		.action.velocity = {                                                               \
			.velocity = 0,                                                             \
			.duration_us = 0,                                                          \
		},                                                                                 \
	}

/**
 * @cond INTERNAL_HIDDEN
 *
 * For internal driver use only, skip these in public documentation.
 */

/** Bit mask for operation mode access in flags. */
#define STEPPER_OP_MODE_MASK                                                                       \
	(STEPPER_OP_MODE_POSITION | STEPPER_OP_MODE_VELOCITY | STEPPER_OP_MODE_ACCELERATION |      \
	 STEPPER_OP_MODE_POSITION_SMOOTH)

/** Get stepper motor operational mode. */
#define STEPPER_OP_MODE_GET(_flags_) ((_flags_) & (STEPPER_OP_MODE_MASK))

/** Bit mask for microstep resolution access in flags. */
#define STEPPER_USTEP_RES_MASK                                                                     \
	(STEPPER_USTEP_RES_1 | STEPPER_USTEP_RES_2 | STEPPER_USTEP_RES_4 | STEPPER_USTEP_RES_8 |   \
	 STEPPER_USTEP_RES_16 | STEPPER_USTEP_RES_32 | STEPPER_USTEP_RES_64 |                      \
	 STEPPER_USTEP_RES_128 | STEPPER_USTEP_RES_256)

/** Get stepper motor microstep resolution. */
#define STEPPER_USTEP_RES_GET(_flags_) ((_flags_) & (STEPPER_USTEP_RES_MASK))

/**
 * @typedef stepper_api_on
 * @brief API for enabling the stepper motor.
 *
 * @see stepper_on() for argument descriptions.
 */
typedef int (*stepper_api_on)(const struct device *dev, const uint8_t motor);

/**
 * @typedef stepper_api_off
 * @brief API for disabling the stepper motor.
 *
 * @see stepper_off() for argument descriptions.
 */
typedef int (*stepper_api_off)(const struct device *dev, const uint8_t motor);

/**
 * @typedef stepper_api_move
 *
 * @brief API for movement according to the provided action.
 *
 * @details If the action includes a duration, this function blocks for that
 * duration. After the duration has passed, the end state of the action
 * persists. For example, a velocity action will last for at least the specified
 * duration, but no 'stop' is implied once the duration has passed. A duration
 * of 0 signifies an indefinite action, e.g. a continuous movement with a
 * constant velocity until a new action is performed. In that case this function
 * does not block.
 *
 * @see stepper_move() for argument descriptions.
 */
typedef int (*stepper_api_move)(const struct device *dev, const uint8_t motor,
				const struct stepper_action *action);

/**
 * @brief Stepper Motor API.
 *
 * @details This is the mandatory API any stepper motor device driver needs
 * to expose.
 */
__subsystem struct stepper_api {
	stepper_api_on on;
	stepper_api_off off;
	stepper_api_move move;
};

/** @endcond */

/**
 * @brief Capabilities of a stepper motor driver chip.
 */
struct stepper_driver_capabilities {
	/** Highest supported full-step rotational speed. */
	const uint32_t fs_max_speed;
	/** Flags describing driver capabilities, such as operation modes and
	    supported microstep resolutions. */
	const uint32_t flags;
};

/**
 * @brief Characteristic properties of a stepper motor.
 */
struct stepper_motor_properties {
	/** Which motor driver output this motor is connected to. */
	const uint8_t index;
	/** Number of full steps for one full turn of the motor shaft. */
	const uint32_t fs_per_turn;
};

/**
 * @brief This structure is common to all stepper motor drivers and is expected
 * to be the first element in the object pointed to by the config field in the
 * device structure.
 */
struct stepper_driver_config {
	/** Number of stepper motors this driver can manage. */
	const size_t n_motors;
	/** Capabilities of this stepper motor driver. */
	const struct stepper_driver_capabilities caps;
	/** Properties of connected motors. */
	const struct stepper_motor_properties *motor_props;
};

/**
 * @brief Container for stepper motor information specified in devicetree.
 */
struct stepper_motor_dt_spec {
	/** The device pointer for the motor driver. */
	const struct device *driver;
	/** The index of this motor output on the given motor driver */
	const uint8_t motor;
	/** Number of full steps for one full turn of the motor shaft. */
	const uint32_t fs_per_turn;
};

#define STEPPER_MOTOR_DT_SPEC_GET_BY_IDX(node_id, idx)                                             \
	STEPPER_MOTOR_DT_SPEC_STRUCT(DT_STEPPER_MOTOR_DRIVER_BY_IDX(node_id, idx),                 \
				     DT_STEPPER_MOTOR_OUTPUT_BY_IDX(node_id, idx))

#define STEPPER_MOTOR_DT_SPEC_GET(node_id) STEPPER_MOTOR_DT_SPEC_GET_BY_IDX(node_id, 0)

/**
 * @brief Initializer for a struct stepper_motor_dt_spec from a stepper motor
 * driver devicetree node and a motor output index
 */
#define STEPPER_MOTOR_DT_SPEC_STRUCT(driver_node, motor_id)                                        \
	{                                                                                          \
		.driver = DEVICE_DT_GET(driver_node), .motor = motor_id,                           \
		.fs_per_turn = DT_PROP(STEPPER_MOTOR_DT_NODE(driver_node, motor_id), fs_per_turn), \
	}

/**
 * @brief Utility macro used by @see STEPPER_MOTOR_DT_NODE that filters child
 * nodes and only returns ones with the specified register address.
 */
#define STEPPER_MOTOR_DT_NODE_FOREACH(motor_node, motor_id)                                        \
	IF_ENABLED(IS_EQ(DT_REG_ADDR(motor_node), motor_id), (motor_node))

/**
 * @brief Get the devicetree node of a single stepper motor attached to a motor
 * driver by output id.
 */
#define STEPPER_MOTOR_DT_NODE(driver_node, motor_id)                                               \
	DT_FOREACH_CHILD_VARGS(driver_node, STEPPER_MOTOR_DT_NODE_FOREACH, motor_id)

/**
 * @brief Initialize a struct stepper_driver_capabilities from a devicetree
 * node.
 *
 * @note The acceleration operating mode that is not (yet) supported is
 * therefore filtered out, @see STEPPER_OP_MODE_ACCELERATION.
 *
 * @param node_id   Devicetree node identifier for the stepper motor
 *                  device whose struct stepper_capabilities to create
 *                  an initializer for.
 * @param flags     The desired flags field in
 *                  struct stepper_driver_capabilities.
 */
#define STEPPER_DRIVER_CAPS_DT(node_id, flags_)                                                    \
	{                                                                                          \
		.fs_max_speed = DT_PROP(node_id, fs_max_speed),                                    \
		.flags = ((STEPPER_OP_MODE_GET((flags_)) | STEPPER_USTEP_RES_GET((flags_))) &      \
			  GENMASK(31, 0)),                                                         \
	}

#define STEPPER_DRIVER_CAPS_DT_INST(inst, flags_) STEPPER_DRIVER_CAPS_DT(DT_DRV_INST(inst), flags_)

/**
 * @brief Initialize a struct stepper_motor_properties from a devicetree node.
 */
#define STEPPER_MOTOR_PROPS_DT(node_id)                                                            \
	{                                                                                          \
		.index = DT_PROP_BY_IDX(node_id, reg, 0),                                          \
		.fs_per_turn = DT_PROP(node_id, fs_per_turn),                                      \
	}

#define STEPPER_MOTOR_PROPS_DT_COMMA(node_id) STEPPER_MOTOR_PROPS_DT(node_id),

#define STEPPER_MOTOR_PROPS_FOREACH_FN(child_node_id)                                              \
	COND_CODE_1(DT_NODE_HAS_PROP(child_node_id, reg),                                          \
		    (STEPPER_MOTOR_PROPS_DT_COMMA(child_node_id)), ())

/**
 * @brief Define an array of struct stepper_motor_properties from the children
 * of a a devicetree node corresponding to a device driver instance.
 *
 * @param inst   The device driver instance identifier.
 * @param props_ Name of the array that will be defined. The instance identifier
 *               is appended to this.
 */
#define STEPPER_MOTOR_PROPS_DT_INST_DEFINE(inst, props_)                                           \
	static const struct stepper_motor_properties props_##inst[] = {                            \
		DT_INST_FOREACH_CHILD(inst, STEPPER_MOTOR_PROPS_FOREACH_FN)};

/**
 * @brief Initialize a struct stepper_driver_config.
 */
#define STEPPER_DRIVER_CONFIG_DT_INST_INITIALIZER(n_motors_, caps_, props_)                        \
	(struct stepper_driver_config)                                                             \
	{                                                                                          \
		.n_motors = n_motors_, .caps = caps_, .motor_props = (props_),                     \
	}

/**
 * @brief Define an instance of struct stepper_driver_config from the devicetree
 * node corresponding to a device driver instance.
 *
 * @param inst        The device driver instance identifier.
 * @param config_     Name of the struct stepper_driver_config that will be
 *                    defined. The device driver instance identifier is
 *                    appended to this.
 * @param caps_flags_ Capability flags to be set for this configuration.
 */
#define STEPPER_DRIVER_CONFIG_DT_INST_DEFINE(inst, config_, caps_flags_)                           \
	STEPPER_MOTOR_PROPS_DT_INST_DEFINE(inst, config_##_motor_props_)                           \
	static const struct stepper_driver_config config_##inst =                                  \
		STEPPER_DRIVER_CONFIG_DT_INST_INITIALIZER(                                         \
			DT_PROP(DT_DRV_INST(inst), nmotors),                                       \
			STEPPER_DRIVER_CAPS_DT_INST(inst, caps_flags_),                            \
			config_##_motor_props_##inst);

/**
 * @brief Get stepper motor driver capabilities
 *
 * Obtain the capabilities of the stepper motor driver, such as operation mode,
 * microstep resolution, highest full-step rotational speed, etc.
 *
 * @param[in] dev Stepper motor device driver instance.
 *
 * @return Stepper motor device driver capabilities.
 */
static inline const struct stepper_driver_capabilities *const
stepper_caps(const struct device *const dev)
{
	const struct stepper_driver_config *const config =
		(struct stepper_driver_config *const)dev->config;

	return &config->caps;
}

/**
 * @brief Get stepper motor properties.
 *
 * @param dev Stepper motor driver instance.
 *
 * @return Stepper motor properties.
 * @retval NULL If no motor properties are found.
 */
static inline const struct stepper_motor_properties *const
stepper_motor_props(const struct device *const dev, uint8_t motor)
{
	const struct stepper_driver_config *const config =
		(struct stepper_driver_config *const)dev->config;

	for (int i = 0; i < config->n_motors; i++) {
		const struct stepper_motor_properties *const props = &config->motor_props[i];
		if (props->index == motor) {
			return props;
		}
	}

	return NULL;
}

/**
 * @brief API for enabling the stepper motor.
 *
 * @details This routine turns on the hardware components that supply
 * the coils of the stepper motor with electrical current.
 *
 * @param[in] dev       Stepper motor device driver instance.
 * @param[in] motor     Stepper motor number.
 *
 * @retval 0            If successful.
 * @retval -ENXIO       If motor is invalid or exceeds hardware capabilities.
 * @return -errno code  on other failure.
 */
__syscall int stepper_on(const struct device *dev, const uint8_t motor);

static inline int z_impl_stepper_on(const struct device *dev, const uint8_t motor)
{
	const struct stepper_api *api = (const struct stepper_api *)dev->api;
	const struct stepper_driver_config *const driver_config =
		(struct stepper_driver_config *)dev->config;

	__ASSERT_NO_MSG(api != NULL);
	__ASSERT_NO_MSG(api->on != NULL);
	__ASSERT_NO_MSG(driver_config != NULL);

	if (!IN_RANGE(motor, 0, driver_config->n_motors - 1)) {
		/* Invalid motor number */
		return -ENXIO;
	}

	return api->on(dev, motor);
}

/**
 * @brief Enables a stepper motor via a struct stepper_motor_dt_spec.
 *
 * @param spec Motor specification from devicetree.
 *
 * @return A value from @see stepper_on().
 */
static inline int stepper_on_dt(const struct stepper_motor_dt_spec *spec)
{
	if (spec == NULL) {
		return -EINVAL;
	}

	return stepper_on(spec->driver, spec->motor);
}

/**
 * @brief API for disabling the stepper motor.
 *
 * @details This routine turns off the hardware components that supply
 * the coils of the stepper motor with electrical current.
 *
 * @param[in] dev       Stepper motor device driver instance.
 * @param[in] motor     Stepper motor number.
 *
 * @retval 0            If successful.
 * @retval -ENXIO       If motor is invalid or exceeds hardware capabilities.
 * @return -errno code  on other failure.
 */
__syscall int stepper_off(const struct device *dev, const uint8_t motor);

static inline int z_impl_stepper_off(const struct device *dev, const uint8_t motor)
{
	const struct stepper_api *api = (const struct stepper_api *)dev->api;
	const struct stepper_driver_config *const driver_config =
		(struct stepper_driver_config *)dev->config;

	__ASSERT_NO_MSG(api != NULL);
	__ASSERT_NO_MSG(api->off != NULL);
	__ASSERT_NO_MSG(driver_config != NULL);

	if (!IN_RANGE(motor, 0, driver_config->n_motors - 1)) {
		/* Invalid motor number */
		return -ENXIO;
	}

	return api->off(dev, motor);
}

/**
 * @brief Disables a stepper motor via a struct stepper_motor_dt_spec.
 *
 * @param spec Motor specification from devicetree.
 *
 * @return A value from @see stepper_off().
 */
static inline int stepper_off_dt(const struct stepper_motor_dt_spec *spec)
{
	if (spec == NULL) {
		return -EINVAL;
	}

	return stepper_off(spec->driver, spec->motor);
}

/**
 * @brief API for flag dependent movement.
 *
 * @details Set the microsteps to be moved from the current absolut position,
 * a.k.a. relative position movement or set the microsteps per second, the
 * absolute velocity, to be used for continuous movement, a.k.a. free running.
 *
 * - @see STEPPER_OP_MODE_POSITION for "positioning mode"
 * - @see STEPPER_OP_MODE_VELOCITY for "velocity mode" (free running)
 *
 * @note The accelerating mode is not (yet) supported.
 *       @see STEPPER_OP_MODE_ACCELERATION for details.
 *
 * @param[in] dev       Stepper motor device driver instance.
 * @param[in] motor     Stepper motor number.
 * @param[in] action    Pointer to the stepper motor action description.
 *
 * @retval 0            If successful.
 * @retval -EIO         If internal I/O operation failure.
 * @retval -ENXIO       If motor is invalid or exceeds hardware capabilities.
 * @retval -EINVAL      If action is invalid or exceeds hardware capabilities.
 * @retval -ENOTSUP     If action or operation mode is not supported.
 * @return -errno code  on other failure.
 */
__syscall int stepper_move(const struct device *dev, const uint8_t motor,
			   const struct stepper_action *action);

static inline int z_impl_stepper_move(const struct device *dev, const uint8_t motor,
				      const struct stepper_action *action)
{
	const struct stepper_api *api = (const struct stepper_api *)dev->api;
	const struct stepper_driver_config *const driver_config =
		(struct stepper_driver_config *)dev->config;
	const struct stepper_driver_capabilities *caps = &driver_config->caps;

	__ASSERT_NO_MSG(api != NULL);
	__ASSERT_NO_MSG(api->move != NULL);
	__ASSERT_NO_MSG(driver_config != NULL);

	if (!IN_RANGE(motor, 0, driver_config->n_motors - 1)) {
		/* Invalid motor number */
		return -ENXIO;
	}

	if ((action->type & STEPPER_OP_MODE_GET(driver_config->caps.flags)) == 0) {
		/* Device doesn't support the requested action type */
		return -ENOTSUP;
	}

	if (STEPPER_USTEP_RES_GET(action->flags) == 0) {
		/* No microstep resolution set */
		return -EINVAL;
	}

	if ((STEPPER_USTEP_RES_GET(action->flags) & STEPPER_USTEP_RES_GET(caps->flags)) == 0) {
		/* Unsupported microstep resolutions set */
		return -EINVAL;
	}

	if (!IS_POWER_OF_TWO(STEPPER_USTEP_RES_GET(action->flags))) {
		/* Multiple microstep resolutions set */
		return -EINVAL;
	}

	if ((action->type == STEPPER_ACTION_TYPE_VELOCITY) &&
	    (!IN_RANGE(labs(action->action.velocity.velocity), 0, caps->fs_max_speed))) {
		/* Invalid (absolute) rotational velocity set */
		return -EINVAL;
	}

	if (action->type == STEPPER_ACTION_TYPE_ACCELERATION) {
		if (!IN_RANGE(labs(action->action.acceleration.start_velocity), 0,
			      caps->fs_max_speed) ||
		    !IN_RANGE(labs(action->action.acceleration.end_velocity), 0,
			      caps->fs_max_speed)) {
			/* Invalid rotational speed */
			return -EINVAL;
		}
	}

	if ((action->type == STEPPER_ACTION_TYPE_POSITIONING_SMOOTH) &&
	    ((!IN_RANGE(action->action.positioning_smooth.max_velocity, 0, caps->fs_max_speed)) ||
	     (action->action.positioning_smooth.acceleration_time_us == 0))) {
		/* Invalid (absolute) rotational velocity or instant acceleration set */
		return -EINVAL;
	}

	return api->move(dev, motor, action);
}

/**

 * @brief Send a move command to a stepper motor via a struct
 stepper_motor_dt_spec.
 *
 * @param spec Motor specification from devicetree.
 * @param action The movement action to perform.
 *
 * @return A value from @see stepper_move().
 */
static inline int stepper_move_dt(const struct stepper_motor_dt_spec *spec,
				  const struct stepper_action *action)
{
	if (spec == NULL) {
		return -EINVAL;
	}

	return stepper_move(spec->driver, spec->motor, action);
}

/**
 * @}
 */

#ifdef __cplusplus
}
#endif

#include <zephyr/syscalls/stepper.h>

#endif /* ZEPHYR_INCLUDE_DRIVERS_STEPPER_H_ */
