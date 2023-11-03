# main.py -- put your code here!

import machine, neopixel, time
import adafruit_sht4x
from adafruit_bme280 import basic as adafruit_bme280
import uasyncio

button = machine.Pin(3, machine.Pin.IN, machine.Pin.PULL_UP)
# button = machine.Pin(3, machine.Pin.IN)
# button = machine.Pin(2, machine.Pin.ALT)
led = neopixel.NeoPixel(machine.Pin(2, machine.Pin.OUT), 1)

i2c = machine.I2C(0, sda=machine.Pin(1), scl=machine.Pin(0), freq=400000)


async def main():
  print('here')
  rht = adafruit_sht4x.SHT4x(i2c)
  prt = adafruit_bme280.Adafruit_BME280(i2c)

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

    temp, humidity = rht.measurements()
    print("Temp/Humidity: {}°C/{}%".format(temp, humidity))
    temp, pressure = prt.measure()
    print("Temp/Pressure: {}°C/{}Pa".format(temp, pressure))
    await uasyncio.sleep(1)

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