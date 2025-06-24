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

## 핀 배치 (Pin Mapping)

| 핀 번호 | 기능                                   |
|-------|--------------------------------------|
| 5     | 윈치 모터 시계 방향 (CW)                |
| 6     | 윈치 모터 반시계 방향 (CCW)            |
| 13    | 스텝 모터 A 위치                       |
| 19    | 스텝 모터 B 위치                       |
| 17    | 금속 감지 센서                         |
| 27    | 안전용 근접 센서                       |
| 22    | 하강 감지 센서                         |
| 26    | 전원 차단 릴레이                       |

각 기능에 대한 한글 주석은 `controller.py` 파일에서도 확인할 수 있습니다.
