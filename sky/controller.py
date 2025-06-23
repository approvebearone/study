import time

"""Raspberry Pi 제어 스크립트

각 클래스와 함수에는 기본 영어 설명과 함께 한글 주석을 추가하여
어떤 핀을 사용하는지와 동작을 이해하기 쉽게 정리했습니다.
"""

try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:  # allows running on machines without GPIO
    from types import SimpleNamespace
    GPIO = SimpleNamespace(BCM=None, OUT=None)
    # 라즈베리파이가 아닌 환경에서 테스트할 수 있도록 간단한 목을 정의한다.
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
    """윈치 모터 제어용 클래스."""

    def __init__(self, cw_pin: int, ccw_pin: int):
        # cw_pin: 시계 방향 제어 핀
        # ccw_pin: 반시계 방향 제어 핀
        self.cw_pin = cw_pin
        self.ccw_pin = ccw_pin
        GPIO.setup(self.cw_pin, GPIO.OUT)
        GPIO.setup(self.ccw_pin, GPIO.OUT)

    def rotate_cw(self):
        """윈치를 시계 방향으로 회전."""
        GPIO.output(self.cw_pin, True)
        GPIO.output(self.ccw_pin, False)

    def rotate_ccw(self):
        """윈치를 반시계 방향으로 회전."""
        GPIO.output(self.cw_pin, False)
        GPIO.output(self.ccw_pin, True)

    def stop(self):
        """모터 정지."""
        GPIO.output(self.cw_pin, False)
        GPIO.output(self.ccw_pin, False)


class StepperMotor:
    """20kgf 스텝 모터 제어용 클래스."""

    def __init__(self, a_pin: int, b_pin: int):
        # a_pin: A 위치 제어 핀
        # b_pin: B 위치 제어 핀
        self.a_pin = a_pin
        self.b_pin = b_pin
        GPIO.setup(self.a_pin, GPIO.OUT)
        GPIO.setup(self.b_pin, GPIO.OUT)

    def move_to_a(self):
        """스텝 모터를 A 위치로 이동."""
        GPIO.output(self.a_pin, True)
        GPIO.output(self.b_pin, False)

    def move_to_b(self):
        """스텝 모터를 B 위치로 이동."""
        GPIO.output(self.a_pin, False)
        GPIO.output(self.b_pin, True)


class Sensor:
    """센서 상태를 추적하기 위한 간단한 래퍼."""

    def __init__(self, pin: int):
        # pin: 센서 입력 핀
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        self.state = False  # 실제 환경에서는 GPIO.input을 사용

    def detected(self) -> bool:
        """센서 감지 여부."""
        return self.state

    def set_state(self, value: bool) -> None:
        """테스트용으로 센서 상태를 설정."""
        self.state = value

    def reset(self) -> None:
        """센서 상태 초기화."""
        self.state = False


class PowerRelay:
    """전원 차단용 릴레이 제어."""

    def __init__(self, pin: int):
        # pin: 릴레이 제어 핀
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)

    def power_off(self):
        """릴레이를 끄고 전원을 차단."""
        GPIO.output(self.pin, False)


class Controller:
    """전체 장치 동작을 관리하는 컨트롤러."""

    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        # 핀 매핑: 사용되는 번호들을 한 곳에 모아 관리
        self.winch = WinchMotor(5, 6)         # 5번: CW, 6번: CCW
        self.stepper = StepperMotor(13, 19)   # 13번: A, 19번: B
        self.metal_sensor = Sensor(17)        # 금속 감지 센서
        self.proximity_sensor = Sensor(27)    # 안전용 근접 센서
        self.descent_sensor = Sensor(22)      # 하강 감지 센서
        self.power_relay = PowerRelay(26)     # 전원 차단 릴레이

    def run(self):
        """메인 동작 루프."""
        while True:
            if self.proximity_sensor.detected():
                # 안전 센서가 트리거되면 전원 차단
                self.power_relay.power_off()
                break

            self.winch.rotate_cw()  # 윈치 모터 시계 방향
            if self.metal_sensor.detected():
                self.stepper.move_to_a()  # 금속 감지 시 스텝 모터 A 위치
            time.sleep(0.5)
            self.winch.rotate_ccw()  # 윈치 모터 반시계 방향

            if self.descent_sensor.detected():
                self.stepper.move_to_b()  # 하강 감지 시 스텝 모터 B 위치
                self.metal_sensor.reset()  # 센서 상태 초기화
                self.descent_sensor.reset()
            time.sleep(0.1)


def main():
    """스크립트 진입점."""
    controller = Controller()
    controller.run()


if __name__ == "__main__":
    main()
