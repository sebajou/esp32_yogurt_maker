# esp32_yogurt_maker
Micropython code and instruction to make a DIY yogurt maker. 

## Project description 

This project is a home made DIY Yogurt maker realise with:
+ esp microcontroler, m5stack esp32 C3 Mate.
+ environement sensor, m5stack ENVIV with a SHT40 sensor and BME280 sensor for temperature and more.
+ relay, 3A relay unit, for provide or cut current for heater
+ a bedside lamp with a Infra Red bulb for heating
+ a camping cooler box, sensor, heater and yogurt will go inside
+ and a bit of micropython code

A Yogurt is made by melt one yogurt for one liter of milk, then by heat it at 40°C during 10 ti 15 hours. This is what this project do. 

## How to do

### Software
See detailed instruction in Usefull command section
1 Shift esp32 in download mode
2 Check devices adress and set file owner
3 Donwload and load the firmware
4 Push the code on esp32 device
5 That's it

### Hardware
1 Command and find every thinks
2 Weld ENV.IV to the microcontroller esp32 C3
3 Weld 3A relay unit to the microcontroller esp32 C3
4 Connect the relay unit to the bedside lamp 
5 Put all inside the a camping cooler box
6 Make the yogurt

## Usefull commands

### Download mode
Before to plus you must enter in the [download mode](https://github.com/gandro/micropython-m5stamp-c3u#enter-download-mode)

### Check devices adress and set file owner
Launch the following command before to plug the devies and after. The pluged devices is the tty* file which appear only on the second command
'''bash
ls /dev/tty*
'''
After devige plug, you will probably need to change owner of the file to be abble to push firmware and code on. 
'''bash
ls -l /dev/ttyACM0
sudo chown jourdan-brutti /dev/ttyACM0
'''

### Donwload and load the firmware
Here you have to downlaod and set up the [firmware](https://github.com/gandro/micropython-m5stamp-c3u#flash-micropython-firmware)

With my m5stack esp 32 C3 mate I first erase the precedent firmware
'''bash
esptool.py -p /dev/ttyACM0 --chip esp32c3 erase_flash
'''

Then load the firmware on the device
'''bash
esptool.py --chip esp32c3 --port /dev/ttyACM0 write_flash -z 0x0 ESP32_GENERIC_C3-20231005-v1.21.0.bin 
'''

### Push the code on esp32 device and deal with files on esp32

Load main.py file and lib folder and contant
'''bash
ampy -d 0.5 --port /dev/ttyACM0 put \main.py
ampy -d 0.5 --port /dev/ttyACM0 put lib
'''

Check if file as here
'''bash
ampy -d 0.5 --port /dev/ttyACM0 ls
ampy -d 0.5 --port /dev/ttyACM0 ls lib
'''

Remove files and folder if necessery
'''bash
ampy --port /dev/ttyACM0 rmdir /lib
ampy --port /dev/ttyACM0 rm /main.py
'''

This lib allow to acces to devices micropython console and interpreter
'''bash 
picocom /dev/ttyACM0 -b115200
'''

This lib can also acces to devices micropython console and interpreter or manage file
'''bash
mpremote a0 cp -r lib :
'''

## Licence

Code under MIT licence
