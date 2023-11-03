# esp32_yogurt_maker
Micropython code and instruction to make a DIY yogurt maker

## Usefull commands

### Check esp32 device adress

For this project I work with m5stack esp32 C3 mate. 

#### Download mode
Before to plus you must enter in the [download mode](https://github.com/gandro/micropython-m5stamp-c3u#enter-download-mode)

#### Check devices adress and set file owner
Launch the following command before to plug the devies and after. The pluged devices is the tty* file which appear only on the second command
'''bash
ls /dev/tty*
'''
After devige plug, you will probably need to change owner of the file to be abble to push firmware and code on. 
'''bash
ls -l /dev/ttyACM0
sudo chown jourdan-brutti /dev/ttyACM0
'''

#### Donwload and load the firmware
Here you have to downlaod and set up the [firmware](https://github.com/gandro/micropython-m5stamp-c3u#flash-micropython-firmware)

With my m5stack esp 32 C3 mate I first erase the precedent firmware
'''bash
esptool.py -p /dev/ttyACM0 --chip esp32c3 erase_flash
'''

Then load the firmware on the device
'''bash
esptool.py --chip esp32c3 --port /dev/ttyACM0 write_flash -z 0x0 ESP32_GENERIC_C3-20231005-v1.21.0.bin 
'''

### Deal with file on device

Load main.py file and lib folder and contant
'''bash
ampy -d 0.5 --port /dev/ttyACM0 put \main.py
ampy -d 0.5 --port /dev/ttyACM0 put \lib
ampy -d 0.5 --port /dev/ttyACM0 ls
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
