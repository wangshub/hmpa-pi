#!/usr/bin/env bash
uname -a

# disable rtl8192 driver
sudo depmod 4.14.79-v7+
sudo rmmod 8192cu
sudo modprobe rtl8192cu

# set monitor mode
sudo ifconfig wlan1 down
sudo iwconfig wlan1 mode monitor
sudo ifconfig wlan1 up