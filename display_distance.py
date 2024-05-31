import time
import board
import serial
import adafruit_us100
from collections import deque
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
#from luma.core.virtual import viewport
#from luma.core.legacy import text, show_message
from luma.core.legacy import text
from luma.core.legacy.font import proportional,LCD_FONT

class DistanceDisplay:
  def __init__(self, serial_port):
    self.ledserial = spi(port=0, device=0, gpio=noop())
    self.device = max7219(
                    self.ledserial, 
                    cascaded=4, 
                    block_orientation=-90,
                    rotate=0, 
                    blocks_arranged_in_reverse_order=False)
    self.uart = serial.Serial(serial_port, baudrate=9600, timeout=1)
    self.us100 = adafruit_us100.US100(self.uart)

    # Set up deque to allow display to blank if the same value is read >= 10 times
    self.q = deque(maxlen=10)
    self.q.append(0)

  def read_and_display(self):
    while True:
      print('------')
      distance = self.us100.distance
      self.q.append(distance)
      dist_str = str(distance)
      dist_len = len(dist_str)
      print(f'Distance: {distance}cm length: {dist_len}')
      # ( Length of string minus decimal point * 5 pixels ) + length of decimal point
      led_len = ((dist_len-1)*5)+4
      with canvas(self.device) as draw:
        # If the queue values are not all the same...
        if not all(i == self.q[0] for i in self.q):
          # Centre the text by taking pixel total (32), subtracting the length of the string (in pixels)
          # and dividing by 2
          # Use proportional font since full width is too big if distance > 100. This does mess up the centring 
          # since '1' is narrower than all other chars but it's not that bad and keeps the calc simple
          text(draw, (((32-led_len)/2), 0), f'{distance}', fill="white", font=proportional(LCD_FONT))
        else:
          # Blank the LED display
          text(draw,(0,0),'',fill="white",font=proportional(LCD_FONT))
      # Sleep for 1 second
      time.sleep(1)

if __name__ == "__main__":
  my_distance_display = DistanceDisplay('/dev/ttyS0')
  my_distance_display.read_and_display()
