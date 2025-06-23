# Sky Project

This folder contains a prototype controller script for a Raspberry Pi based
system that manages motors and sensors. The workflow is based on the sequence
provided in the project description and uses `RPi.GPIO` for actual hardware.

If executed on a non-Raspberry Pi machine, the script will fall back to a
simple mock of the GPIO interface so that the program can run for testing
purposes without real hardware.

## How to run
```bash
python sky/controller.py
```
This will start the control loop. The logic performs:
1. Rotate the winch motor clockwise.
2. When the metal sensor triggers, move the stepper motor to position A.
3. After a brief pause, run the winch motor counter-clockwise.
4. When the descent sensor triggers, move the stepper motor to position B and
   reset both sensors.
5. If the safety proximity sensor activates, the power relay is turned off and
   the loop exits.
```
