/*******************************************************************************
Author: David Vazquez Garcia -- davidvazquez.gijon@gmail.com


The library SkyPointer_MotorShield can be downloaded from:
    https://github.com/davidvg/SkyPointer_MotorShield

*******************************************************************************/

#include <SoftwareSerial.h>
#include <SerialCommand.h>
#include <Wire.h>
#include <SkyPointer_MotorShield.h>
#include <TimerOne.h>
#include <EEPROM.h>

// A modulo operator that handles negative numbers
#define MOD(a,b) ((((a)%(b))+(b))%(b))

// Motor parameters
#define STEPS 200
#define USTEPS 16
#define TOTAL_USTEPS (STEPS*USTEPS)

// Speed parameters
#define DT 10000 // Timer1 interrupt period
//#define RPM 1   // Desired rotation speed in rpm

// Define pins
#define LASER_PIN 13
#define PHOTO_PIN A0

// Define how long the laser stays on when the target has been reached
#define LASER_T_ON 4000000  // 4 seconds

//#define DEBUG_ISR 1  // Variable for Interruption debug
// Pin for DEBUG_ISR
#ifdef DEBUG_ISR
  int blinkLed = 12;
#endif

#define DEBUG_L 1      // Variable for Laser debug
#ifndef DEBUG_ISR      // Check that ISR debug is off
#ifdef DEBUG_L
  int laser_dbg = 12;
#endif
#endif

// Definition of the SerialCommand object
SerialCommand sCmd;
// Definition of the motor shield
SkyPointer_MotorShield MS = SkyPointer_MotorShield();
// Motor 1 on port 1, 200 steps/rev
SkyPointer_MicroStepper *motor1 = MS.getMicroStepper(STEPS, 1);
// Motor 2 on port 2, 200 steps/rev
SkyPointer_MicroStepper *motor2 = MS.getMicroStepper(STEPS, 2);

int home = false;

/****************************************************************************/
// Timing routine
void ISR_timer(){
  // Check if the time the laser has been pointing to the object is equal to
  // the desired ON time
  uint32_t t_on = MS.getTimeOn(); // Get the stored value for laser_t_on
  if (t_on >= LASER_T_ON){
    digitalWrite(LASER_PIN, LOW); // Turn off the laser
    Timer1.detachInterrupt();     // Detach interruption
  }
  MS.setTimeOn(t_on + uint32_t(DT));// Increment with the current time

}


// Interruption routine
void ISR_rotate() {
  #ifdef DEBUG_ISR
    // Turns the LED on when entering the ISR
    // Measures the duration of the interruption routine
    digitalWrite (blinkLed, HIGH);
  #endif

  uint16_t pos, sim_pos, tg;
  uint8_t dir;

  // Turn on the laser
  digitalWrite(LASER_PIN, HIGH);


  sei();  // Enable interrupts --> Serial, I2C (MotorShield)

  // MOTOR 1
  pos = motor1->getPosition();
  // Calculate simmetric point to current position
  sim_pos = (pos + TOTAL_USTEPS/2) % TOTAL_USTEPS;
  tg = motor1->target;

  if (!motor1->isTarget()) {  // Check target has not been reached
    if (pos < TOTAL_USTEPS/2) {
      dir = ((tg > pos) && (tg < sim_pos)) ? FORWARD : BACKWARD;
    } else {
      dir = ((tg > pos) || (tg < sim_pos)) ? FORWARD : BACKWARD;
    }
    motor1->microstep(1, dir);
  }

  // MOTOR 2
  pos = motor2->getPosition();
  // Calculate simmetric point to current position
  sim_pos = (pos + TOTAL_USTEPS/2) % TOTAL_USTEPS;
  tg = motor2->target;

  if (home) {
    // if homing, move motor2 until the photodiode gets interrupted
    if (analogRead(PHOTO_PIN) < 512) {
      motor2->microstep(1, BACKWARD);
    } else {
      motor2->setPos(0);
      home = false;
    }
  } else {
    if (!motor2->isTarget()) {  // Check target has not been reached
      if (pos < TOTAL_USTEPS/2) {
        dir = ((tg > pos) && (tg < sim_pos)) ? FORWARD : BACKWARD;
      } else {
        dir = ((tg > pos) || (tg < sim_pos)) ? FORWARD : BACKWARD;
      }
      motor2->microstep(1, dir);
    }
  }

  // Check if target is reached
  if ((motor1->isTarget()) && (motor2->isTarget())) {
    // If both motors are in the target position...
    Timer1.detachInterrupt();	// Stop Timer1 interruption
    // TURN OFF THE LASER
    //digitalWrite(LASER_PIN, LOW);
    MS.setTimeOn(uint32_t(0));          // Set timer to current time
    Timer1.attachInterrupt(ISR_timer); // Attach temporization routine

    // Must check a global variable that contains the status of the laser, ON
    // or OFF, so the program cannot turn it off if it has been turned on by
    // choice. This variable is not yet defined.
  }

  #ifdef DEBUG_ISR
    digitalWrite (blinkLed, LOW);   // Turn the LED off in ISR exit
  #endif
}

/*******************************************************************************
 * Functions for processing the commands received via serial port
 ******************************************************************************/

// Update the target positions for both motors
void ProcessGoto() {
  uint16_t tgt1, tgt2;

  tgt1 = MOD(atoi(sCmd.next()), TOTAL_USTEPS);
  tgt2 = MOD(atoi(sCmd.next()), TOTAL_USTEPS);

  motor1 -> setTarget(tgt1);
  motor2 -> setTarget(tgt2);

  Serial.print("OK\r");
  Timer1.attachInterrupt(ISR_rotate);  // Enable TimerOne interruption
}


// Move both motors to a relative position
void ProcessMove() {
  uint16_t tgt1, tgt2;

  tgt1 = MOD((int16_t)motor1->getPosition() + atoi(sCmd.next()), TOTAL_USTEPS);
  tgt2 = MOD((int16_t)motor2->getPosition() + atoi(sCmd.next()), TOTAL_USTEPS);

  motor1 -> setTarget(tgt1);
  motor2 -> setTarget(tgt2);

  Serial.print("OK\r");
  Timer1.attachInterrupt(ISR_rotate);  // Enable TimerOne interruption
}


// Stop both motors
void ProcessStop() {
  motor1 -> setTarget(motor1->getPosition());
  motor2 -> setTarget(motor2->getPosition());

  Serial.print("OK\r");
  Timer1.attachInterrupt(ISR_rotate);  // Enable TimerOne interruption
}


// Go to home position (elevation motor only)
void ProcessHome() {
  home = true;
  Serial.print("OK\r");
  Timer1.attachInterrupt(ISR_rotate);  // Enable TimerOne interruption
}


// Get the current position of the motors
void ProcessGetPos() {
  char buf[13];
  uint16_t tgt1, tgt2;

  tgt1 = motor1->getPosition();
  tgt2 = motor2->getPosition();

  sprintf(buf, "P %04d %04d\r", tgt1, tgt2);
  Serial.print(buf);
}


// Enable/disable the laser module
void ProcessLaser() {
  uint8_t enable;

  enable = atoi(sCmd.next()) != 0;
  digitalWrite(LASER_PIN, enable);
  Serial.print("OK\r");
}


// Release motors and shut down laser
void ProcessQuit() {
  motor1->release();
  motor2->release();
  digitalWrite(LASER_PIN, 0);
  Serial.print("OK\r");
}


// Get ID
void ProcessID() {
  Serial.print("SkyPointer 1.0\r");
}


// Write a calibration value (4 bytes) to EEPROM
void ProcessWriteCalib () {
  uint8_t n = atoi(sCmd.next());
  if (n > 3) {
      Serial.print("NK\r");
      return;
  }

  char data[4];
  sscanf(sCmd.next(), "%lx", (uint32_t *)data);
  for (int i = 0; i < 4; i++) {
    EEPROM.write(4*n + i, data[i]);
  }
  Serial.print("OK\r");
}


// Read a calibration value (4 bytes) from EEPROM
void ProcessReadCalib () {
  uint8_t n = atoi(sCmd.next());
  if (n > 3) {
      Serial.print("NK\r");
      return;
  }

  char buf[12], data[4];
  for (int i = 0; i < 4; i++) {
    data[i] = EEPROM.read(4*n + i);
  }
  sprintf(buf, "R %08lx\r", *(uint32_t *)data);
  Serial.print(buf);
}


// Handles unknown commands
void Unrecognized() {
  Serial.print("NK\r");
}
/****************************************************************************/

void setup() {
  // Configure laser pin and set to LOW
  pinMode(LASER_PIN, OUTPUT);
  digitalWrite(LASER_PIN, LOW);
  #ifdef DEBUG_ISR
    pinMode (blinkLed, OUTPUT);
    digitalWrite (blinkLed, LOW);   // Turn off the LED
  #endif

  // Start the serial port
  Serial.begin(115200);

  // Add the commands to the SerialCommand object
  sCmd.addCommand("G", ProcessGoto);    // G pos1 pos2\r
  sCmd.addCommand("M", ProcessMove);    // M steps1 steps2\r
  sCmd.addCommand("S", ProcessStop);    // S\r
  sCmd.addCommand("P", ProcessGetPos);  // P\r
  sCmd.addCommand("H", ProcessHome);    // H\r
  sCmd.addCommand("L", ProcessLaser);   // L enable\r
  sCmd.addCommand("I", ProcessID);      // I\r
  sCmd.addCommand("W", ProcessWriteCalib); // Write calibration value to EEPROM
  sCmd.addCommand("R", ProcessReadCalib);  // Read calibration value from EEPROM
  sCmd.addCommand("Q", ProcessQuit);    // Release motors and shut down laser
  sCmd.addDefaultHandler(Unrecognized);	// Unknown commands

  // Configure interrupt speed (microseconds)
  Timer1.initialize(DT);

  // Start motor shield
  MS.begin();
  //motor1->setSpeed(RPM);
  //motor2->setSpeed(RPM);
}

void loop() {
  sCmd.readSerial();  // Read commands from serial port
}
