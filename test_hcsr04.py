import board
from adafruit_hcsr04 import HCSR04
from time import sleep
with HCSR04(trigger_pin=board.D2,echo_pin=board.D3) as sonar:
  try:
    while True:
      try:
        distance = sonar.distance
        print(f'{round(sonar.distance,1)}')
      except RuntimeError as e:
        print(f'Timed out: {e}')
      finally:
        sleep(2)
  except KeyboardInterrupt:
    pass
