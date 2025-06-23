import time

try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:  # allows running on machines without GPIO
    from types import SimpleNamespace
    GPIO = SimpleNamespace(BCM=None, OUT=None)
    def setup(*args, **kwargs):
        pass
    def output(*args, **kwargs):
        print("GPIO output", args, kwargs)
    def setwarnings(flag):
        pass
    GPIO.setmode = setup
    GPIO.setup = setup
    GPIO.output = output
    GPIO.setwarnings = setwarnings


class WinchMotor:
    def __init__(self, cw_pin: int, ccw_pin: int):
        self.cw_pin = cw_pin
        self.ccw_pin = ccw_pin
        GPIO.setup(self.cw_pin, GPIO.OUT)
        GPIO.setup(self.ccw_pin, GPIO.OUT)

    def rotate_cw(self):
        GPIO.output(self.cw_pin, True)
        GPIO.output(self.ccw_pin, False)

    def rotate_ccw(self):
        GPIO.output(self.cw_pin, False)
        GPIO.output(self.ccw_pin, True)

    def stop(self):
        GPIO.output(self.cw_pin, False)
        GPIO.output(self.ccw_pin, False)


class StepperMotor:
    def __init__(self, a_pin: int, b_pin: int):
        self.a_pin = a_pin
        self.b_pin = b_pin
        GPIO.setup(self.a_pin, GPIO.OUT)
        GPIO.setup(self.b_pin, GPIO.OUT)

    def move_to_a(self):
        GPIO.output(self.a_pin, True)
        GPIO.output(self.b_pin, False)

    def move_to_b(self):
        GPIO.output(self.a_pin, False)
        GPIO.output(self.b_pin, True)


class Sensor:
    def __init__(self, pin: int):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        self.state = False

    def detected(self):
        return self.state

    def set_state(self, value: bool):
        self.state = value

    def reset(self):
        self.state = False


class PowerRelay:
    def __init__(self, pin: int):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)

    def power_off(self):
        GPIO.output(self.pin, False)


class Controller:
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        self.winch = WinchMotor(5, 6)
        self.stepper = StepperMotor(13, 19)
        self.metal_sensor = Sensor(17)
        self.proximity_sensor = Sensor(27)
        self.descent_sensor = Sensor(22)
        self.power_relay = PowerRelay(26)

    def run(self):
        while True:
            if self.proximity_sensor.detected():
                self.power_relay.power_off()
                break

            self.winch.rotate_cw()
            if self.metal_sensor.detected():
                self.stepper.move_to_a()
            time.sleep(0.5)
            self.winch.rotate_ccw()

            if self.descent_sensor.detected():
                self.stepper.move_to_b()
                self.metal_sensor.reset()
                self.descent_sensor.reset()
            time.sleep(0.1)


def main():
    controller = Controller()
    controller.run()


if __name__ == "__main__":
    main()
