/******************************************************************
Author:    David Vazquez Garcia    <davidvazquez.gijon@gmail.com>
           Juan Menendez Blanco    <juanmb@gmail.com>
Version:   1.0
Date:      2016/Apr/08

This code is an adaptation of the Adafruit library for the Adafruit Motor
Shield V2 motor driver for Arduino [1]

The library implements some new methods and variables for the specific use in
the SkyPointer project [2]. Stepper and DC motor control have been removed.

----

This code has been adapted from the library for the Adafruit Motor
Shield V2 for Arduino.

It supports DC motors & Stepper motors with microstepping as well
as stacking-support. It is *not* compatible with the V1 library!

It will only work with https://www.adafruit.com/products/1483

Adafruit invests time and resources providing this open
source code, please support Adafruit and open-source hardware
by purchasing products from Adafruit!

Written by Limor Fried/Ladyada for Adafruit Industries.
BSD license, check license.txt for more information.
All text above must be included in any redistribution.

Reference:
[1]  https://www.adafruit.com/products/1483
[2]  https://github.com/juanmb/SkyPointer
*******************************************************************************/
#ifndef _SkyPointer_MotorShield_h_
#define _SkyPointer_MotorShield_h_

#include <inttypes.h>
#include <Wire.h>
#include "utility/Adafruit_PWMServoDriver.h"

// Number of microsteps per step
#define MICROSTEPS 16
// Definition of directions for the rotation
#define FORWARD 1
#define BACKWARD 2
// Definition of the two possible Laser pins, depending on its type
#define LASER_PIN_H 13
#define LASER_PIN_L 12


// Predefinition of the SkyPointer_MotorShield for its use in the Microstepper
class SkyPointer_MotorShield;


// New class for Microstepper motor
class SkyPointer_MicroStepper {
    public:
        SkyPointer_MicroStepper (void); // Constructor for the class
        friend class SkyPointer_MotorShield;

        uint16_t target;            // Target position for the motor

        void setPos(uint16_t);      // Sets the current position
        uint16_t getPosition ();    // Returns current position of the motor
        void setTarget(uint16_t);   // Sets the value of the target for the motor
        boolean isTarget(void);     // Returns True if currPos == target
        void setSpeed(float);       // Sets the speed of the motor ## TO-DO ##
        uint32_t getSpeed();        // Returns the speed of the motor in us

        // Function for a rotation of one microstep in any direction
        uint16_t microstep (uint16_t usteps, uint8_t dir);
        // Removes voltage from the coils
        void release (void);

    private:
        uint32_t usecPerMicrostep;  // Time interval between rotations to rotate
                                    // at the desired speed
        uint8_t microsteppernum;    // Stores the number of the motor [1, 2]
        uint16_t microstepsPerRev;  // Number of steps per rev times microsteps
                                    // per step
        uint16_t currMicrostep;     // Current microstep in the cycle of a step
                                    // It's a value in [0, MICROSTEPS]
        uint16_t currPos;           // Current position in the revolution

        // Variables for the PWM
        uint8_t PWMApin, AIN1pin, AIN2pin;
        uint8_t PWMBpin, BIN1pin, BIN2pin;

        SkyPointer_MotorShield *MC;
};


class SkyPointer_MotorShield {
    public:
        // Constructor for the class
        SkyPointer_MotorShield(uint8_t addr = 0x60);
        
        // Attach stepper motor in microstepper mode
        SkyPointer_MicroStepper *getMicroStepper(uint16_t, uint8_t);

        void begin(uint16_t freq = 1600); // Initializes the shield
        void setPWM(uint8_t, uint16_t);   // Function for the PWM's config
        void setPin(uint8_t, boolean);    // Function for the PWM's config
	    void setTimeOn(uint32_t);         // Stores elapsed ON time for laser
        uint32_t getTimeOn(void);         // Returns elapsed ON time for laser
        void laser(uint8_t);              // Turn on/off the laser

    private:
        SkyPointer_MicroStepper microsteppers[2]; // Array to store the motors
                                                  // in microstep mode
        uint8_t _addr;                    // Internal variable for driver
        uint16_t _freq;                   // Internal variable for driver

	    uint32_t laser_t_on;              // Elapsed ON time for laser
        Adafruit_PWMServoDriver _pwm;     // Internal driver object
};

#endif
