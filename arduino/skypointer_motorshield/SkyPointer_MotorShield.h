/******************************************************************
 This code has been adapter from the library for the
 Adafruit Motor Shield V2 for Arduino.
 It supports DC motors & Stepper motors with microstepping as well
 as stacking-support. It is *not* compatible with the V1 library!

 It will only work with https://www.adafruit.com/products/1483

 Adafruit invests time and resources providing this open
 source code, please support Adafruit and open-source hardware
 by purchasing products from Adafruit!

 Written by Limor Fried/Ladyada for Adafruit Industries.
 BSD license, check license.txt for more information.
 All text above must be included in any redistribution.
*******************************************************************/
#ifndef _SkyPointer_MotorShield_h_
#define _SkyPointer_MotorShield_h_

#include <inttypes.h>
#include <Wire.h>
#include "utility/Adafruit_PWMServoDriver.h"

#define MICROSTEPS 16         // 8 or 16


// REMOVE ???
/*
#define MOTOR1_A 2
#define MOTOR1_B 3
#define MOTOR2_A 1
#define MOTOR2_B 4
#define MOTOR4_A 0
#define MOTOR4_B 6
#define MOTOR3_A 5
#define MOTOR3_B 7
*/

// REMOVE BRAKE AND RELEASE ???
#define FORWARD 1
#define BACKWARD 2
//#define BRAKE 3
//#define RELEASE 4

// Not needed for the MicroStepper class.
// Used only in the Stepper class
#define SINGLE 1
#define DOUBLE 2
#define INTERLEAVE 3
#define MICROSTEP 4

/******************************************************************************/

// Predefinition of the SkyPointer_MotorShield for its use in the Microstepper
class SkyPointer_MotorShield;

/******************************************************************************/

// New class for Microstepper motor
class SkyPointer_MicroStepper {
    public:
        SkyPointer_MicroStepper (void); // Constructor for the class
        friend class SkyPointer_MotorShield;

        uint16_t getPosition ();    // Returns current position of the motor
        uint16_t target;            // Target position for the motor
        void setTarget(uint16_t);   // Sets the value of the target for the motor
        void setPos(uint16_t);      // Sets the current position
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

/******************************************************************************/
//  TO-DO -- Make cleanup
/*
class SkyPointer_StepperMotor {
 public:
  SkyPointer_StepperMotor(void);
  friend class SkyPointer_MotorShield;

  void step(uint16_t steps, uint8_t dir,  uint8_t style = SINGLE);

  void setSpeed(uint16_t);
  uint8_t onestep(uint8_t dir, uint8_t style);
  void release(void);
  uint32_t usperstep, steppingcounter;

 private:
  uint8_t PWMApin, AIN1pin, AIN2pin;
  uint8_t PWMBpin, BIN1pin, BIN2pin;
  uint16_t revsteps; // # steps per revolution
  uint8_t currentstep;
  SkyPointer_MotorShield *MC;
  uint8_t steppernum;
};
*/

/******************************************************************************/

class SkyPointer_MotorShield {
    public:
        // Constructor for the class
        SkyPointer_MotorShield(uint8_t addr = 0x60);

        void begin(uint16_t freq = 1600);       // Initializes the shield
        // Functions for setting PWM
        void setPWM(uint8_t pin, uint16_t val);
        void setPin(uint8_t pin, boolean val);

        // Attach stepper motor in microstepper mode
        SkyPointer_MicroStepper *getMicroStepper(uint16_t steps, uint8_t num);
        // Attach stepper motor in normal mode
        //SkyPointer_StepperMotor *getStepper(uint16_t steps, uint8_t n);

        // Variable for setting the value for laser_t_on
	    void setTimeOn(uint32_t);
        // Variable for getting the value for laser_t_on
        uint32_t getTimeOn(void);

    private:
        SkyPointer_MicroStepper microsteppers[2];   // Array to store the motors
                                                    // in microstep mode
        //SkyPointer_StepperMotor steppers[2];        // Array to store the motors
                                                    // in normal mode
        // Variables for setting the board
        uint8_t _addr;
        uint16_t _freq;

        // Variable for checking the ON time for the laser
	    uint32_t laser_t_on;

        Adafruit_PWMServoDriver _pwm;
};

#endif
