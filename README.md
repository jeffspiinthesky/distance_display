# Distance Display
## Description
This project uses a PI Zero W, a US100 Ultrasonic sensor and an LED Matrix display to measure how far away my car is from an obstruction.

## Kit List
* Raspberry PI Zero W or above (https://thepihut.com/products/raspberry-pi-zero-w)
* US100 Ultrasonic Sensor (https://thepihut.com/products/us-100-ultrasonic-distance-sensor-3v-or-5v-logic)
* LED Matrix display (https://www.amazon.co.uk/dp/B099F1YPQZ)
* Jumper wires to use as extensions (https://www.amazon.co.uk/dp/B07GN85RC2)

## OS Install & Firmware
### Install OS
* Burn Raspberry PI OS Lite 32 Bit to a micro SD card (use 64-bit if using a PI3 or above)
* Boot PI from it
### Increase swap size (only required on PI Zero W, PI Zero 2W or PI2)
```
sudo dphys-swapfile swapoff
sudo vi /etc/dphys-swapfile
```
Set the value for the parameter CONF_SWAPSIZE to 2048 and save the file
```
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
```
### Increase over_voltage, force_turbo, and enable UART
NOTE: over_voltage and force_turbo only required on PI Zero W, PI Zero 2W, PI1 or PI2
```
sudo vi /boot/firmware/config.txt
```
Scroll all  the way to the bottom of the file and add:
```
over_voltage=6
force_turbo=1
enable_uart=1
```
Save the file and reboot
### Update firmware
```
sudo rpi-update
```
Reboot when complete
### Enable SPI
```
sudo raspi-config
```
* Navigate to Interfaces -> SPI
* Enable SPI
```
sudo usermod -aG spi,gpio pi
```
Reboot when complete

### Install all dependencies
```
sudo apt install build-essential python3-dev python3-pip libfreetype6-dev libjpeg-dev libopenjp2-7 libtiff6
python -m venv --system-site-packages venv
source venv/bin/activate
pip install --upgrade --ignore-installed pip setuptools
pip install --upgrade luma.led_matrix
pip install adafruit-circuitpython-us100
```
### Connect devices
Connect the LED Matrix and US-100 to the GPIO pins shown below:
* LED Matrix
  * VCC (Voltage In) = 4
  * GND (Ground) = 14
  * DIN (Data In) = 19
  * CS (Chip Select) = 24
  * CLK (Clock) = 23
* US100
  * VCC (Voltage In) = 2
  * TX (Transmit) = 8
  * RX (Receive) = 10
  * GND (Ground) = 6
### Clone this code
```
git clone https://github.com/jeffspiinthesky/distance_display.git
```
### Test
```
python display_distance.py
```
You should get output such as:
```
------
Distance: 17.1cm length: 4
------
Distance: 9.6cm length: 3
------
Distance: 4.2cm length: 3
...etc
```
CTRL-c to stop it
### Enable service
```
sudo cp display_distance.service /usr/lib/systemd/system/
sudo systemctl enable display_distance
```
## ENJOY!!!
sudo systemctl start display_distance
