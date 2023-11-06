# main.py -- put your code here!

import machine, neopixel, time
from lib import sht4x
from lib import bme280_float as bme280
import uasyncio

button = machine.Pin(3, machine.Pin.IN, machine.Pin.PULL_UP)
relay = machine.Pin(19, Pin.OUT)
led = neopixel.NeoPixel(machine.Pin(2, machine.Pin.OUT), 1)

i2c = machine.I2C(0, sda=machine.Pin(1), scl=machine.Pin(0), freq=400000)


async def main():
  print('here')
  sht = sht4x.SHT4X(i2c)
  bme = bme280.BME280(i2c=i2c)

  while True:
    print('in the best loop')
    led.write()
    time.sleep_ms(500)
    led.fill((250, 16, 16))
    led.write()
    time.sleep_ms(500)
    led.fill((16, 250, 16))
    led.write()
    time.sleep_ms(500)

    temp, humidity = sht.measurements
    print("Temp/Humidity: {}°C/{}%".format(temp, humidity))
    tempbme, pressure, humiditybme = bme.read_compensated_data()
    altitude = bme.altitude
    print("Temp/Pressure/altitude/humidity: {}°C/{}Pa/{}m/{}%".format(tempbme, pressure, altitude, humiditybme))
    await uasyncio.sleep(1)

    if temp > 42:
      # Stop relay
      relay.value(1)
    elif temp < 40:
      # Start relay
      relay.value(0)
    else:
      continue

    if button.value() == 0:
      led.fill((99, 99, 5))
      led.write()
      time.sleep_ms(500)
      print('go out the loop')
      await uasyncio.sleep(1)
      break

  led.fill((0, 0, 0))
  led.write()

uasyncio.run(main())