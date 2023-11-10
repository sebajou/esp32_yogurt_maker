# Copyright (c) 2022 Sebastian Jourdan
# SPDX-License-Identifier: MIT

# MicroPython import 
import machine, neopixel, time
import network
import uasyncio

# Sensor
from lib import sht4x
from lib import bme280_float as bme280

# Home Assistant
from homeassist import HomeAssistant, Sensor

# Configuration constant
from config import cfg

# Esp32 setup
button = machine.Pin(3, machine.Pin.IN, machine.Pin.PULL_UP)

led = neopixel.NeoPixel(machine.Pin(2, machine.Pin.OUT), 1)
i2c = machine.I2C(0, sda=machine.Pin(1), scl=machine.Pin(0), freq=400000)
print("Esp32 setup")

async def main():
  print('Start Yogurt maker program')

  # Wifi network managment
  try: 
    print("Connecting to network...")
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(cfg["wifi_ssid"], cfg["wifi_key"])
    countLoop = 1
    while not wifi.isconnected() or countLoop < 5:
      time.sleep_ms(500)
      print("Wifi connecting ...")
      countLoop += 1
    if wifi.isconnected():
      print("Wifi connected")
    else:
      print("Wifi connection not successfull")
  except Exception as e:
    # TODO sauvage except to improve
    print(f"Wifi connection failllure with the following error: {e}") 

  try: 
    # Home Assistant setup
    ha = HomeAssistant(cfg["ha_host"], cfg["ha_port"], cfg["ha_ssl"], cfg["ha_token"])
    temp_sht_sensor = Sensor(
        "temp", "°C", "temperature", "Temperature")
    humidity_sht_sensor = Sensor(
        "humidity", "%", "humidity", "Humidity")
    temp_bme_sensor = Sensor(
        "tempbme", "°C", "temperature", "Temperature")
    pressure_bme_sensor = Sensor(
        "pressure", "Pa", "pressure", "Pressure")
    altitude_bme_sensor = Sensor(
        "altitude", "m", "altitude", "Altitude")
    yogurt_time_renaining = Sensor(
        "timeremaining", "hours", "yogurt_time_renaining", "yogurt_time_renaining")
    print("Home Assistant setup success")
  except Exception as e:
    # TODO sauvage except to improve
    print(f"Maybe a Home Assisstant Setting issue with the following error: {e}")

  try: 
    # Sensor setup
    print("Start sensor setup")
    sht = sht4x.SHT4X(i2c)
    bme = bme280.BME280(i2c=i2c)

    # await sht.start()
    # await bme.start()
    print("Sensor setup success")

    # Time for make yogurt: 14 hours or 50400.0 seconds
    currenttime = time.time()
    # TODO allow to change timetomakeyogurt programmaticaly and improve time display
    timetomakeyogurt = 50400.0
    endyogurttime = currenttime + timetomakeyogurt
    print(f"Yogurt time set up, start at {currenttime}, duration: {timetomakeyogurt}, end at {endyogurttime}")

    while True:
    
      # Time count
      timeremaining = (endyogurttime - time.time())/ (60*60)
      print(f'Start mesureaments, {timeremaining} hours remaining')
      
      # Green led for ongoing mesurements
      led.write()
      time.sleep_ms(500)
      led.fill((16, 250, 16))
      led.write()
      time.sleep_ms(500)

      # Sensor mesurement
      temp, humidity = sht.measurements
      print("Temp/Humidity: {}°C/{}%".format(temp, humidity))
      tempbme, pressure, humiditybme = bme.read_compensated_data()
      altitude = bme.altitude
      print(f"Temp/Pressure/altitude: {tempbme}°C/{pressure}Pa/{altitude}m")
      
      try:
        # Information send to Home Assistant
        await ha.submit(temp_sht_sensor, temp)
        await ha.submit(humidity_sht_sensor, humidity)
        await ha.submit(temp_bme_sensor, tempbme)
        await ha.submit(pressure_bme_sensor, pressure)
        await ha.submit(altitude_bme_sensor, altitude)
        await ha.submit(yogurt_time_renaining, timeremaining)
        await uasyncio.sleep(1)
      except Exception as e:
        # TODO sauvage except to improve
        print(f"Maybe fail to send to Home Assistant or HA error with the following error: {e}")

      # Control of Heater through relay control
      relay = machine.Pin(9, machine.Pin.OUT)
      if temp > 42:
        print(f"Temperature at {temp} up to 42°C, stoping relay for stop heater")
        led.write()
        time.sleep_ms(500)
        led.fill((16, 16, 250))
        led.write()
        time.sleep_ms(500)
        relay.value(0)
      elif temp < 41:
        print(f"Temperature at {temp} under 40°C, starting the relay for start heater")
        led.write()
        time.sleep_ms(500)
        led.fill((250, 16, 16))
        led.write()
        time.sleep_ms(500)
        relay.value(1)
      else:
        # between 41 and 42 we do nothing
        print(f"Temperature at {temp} between 41°C and 42°C, staying with same state for the relay")
        led.write()
        time.sleep_ms(500)
        led.fill((200, 200, 16))
        led.write()
        time.sleep_ms(500)
        pass

      # Excape to the while when press central button or at the end of timetomakeyogurt
      if button.value() == 0 or timeremaining < 0.0:
        led.fill((99, 99, 5))
        led.write()
        time.sleep_ms(500)
        relay.value(0)
        print('Stop the process')
        await uasyncio.sleep(1)
        break
  
  except Exception as e:
    # TODO sauvage except to improve
    print(f"Probably sensor connection default with the following error: {e}")
  
  # Extinguish led before to stop
  led.fill((0, 0, 0))
  led.write()

uasyncio.run(main())