import machine, neopixel, time
from lib import sht4x
from lib import bme280_float as bme280
import uasyncio

button = machine.Pin(3, machine.Pin.IN, machine.Pin.PULL_UP)
relay = machine.Pin(9, machine.Pin.OUT)
led = neopixel.NeoPixel(machine.Pin(2, machine.Pin.OUT), 1)
currenttime = time.time()
endyogurttime = currenttime + 50400.0
i2c = machine.I2C(0, sda=machine.Pin(1), scl=machine.Pin(0), freq=400000)


async def main():
  print('here')
  try: 
    sht = sht4x.SHT4X(i2c)
    bme = bme280.BME280(i2c=i2c)


    while True:
      timeremaining = (time.time() - endyogurttime)/ (60*60)
      print('Start mesureaments, {timeremaining} hours remaining', timeremaining)
      led.write()
      time.sleep_ms(500)
      led.fill((16, 250, 16))
      led.write()
      time.sleep_ms(500)

      temp, humidity = sht.measurements
      print("Temp/Humidity: {}°C/{}%".format(temp, humidity))
      tempbme, pressure, humiditybme = bme.read_compensated_data()
      altitude = bme.altitude
      print("Temp/Pressure/altitude: {}°C/{}Pa/{}m".format(tempbme, pressure, altitude))
      await uasyncio.sleep(1)

      if temp > 42:
        print(f"Temperature at {temp} up to 42°C, stoping relay for stop heater", temp)
        led.write()
        time.sleep_ms(500)
        led.fill((16, 16, 250))
        led.write()
        time.sleep_ms(500)
        relay.value(0)
      elif temp < 40:
        print(f"Temperature at {temp} under 40°C, starting the relay for start heater", temp)
        led.write()
        time.sleep_ms(500)
        led.fill((250, 16, 16))
        led.write()
        time.sleep_ms(500)
        relay.value(1)
      else:
        pass

      if button.value() == 0 or time.time == endyogurttime:
        led.fill((99, 99, 5))
        led.write()
        time.sleep_ms(500)
        relay.value(0)
        print('Stop the process')
        await uasyncio.sleep(1)
        break
  
  except:
    print("Probably sesor connection default")
  
  led.fill((0, 0, 0))
  led.write()

uasyncio.run(main())