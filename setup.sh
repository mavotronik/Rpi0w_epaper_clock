#!/bin/bash

sudo apt update 
sudo apt install git  python3-pip python3-numpy python3-pillow -y

pip3 install RPi.GPIO spidev --break-system-packages

git clone https://github.com/waveshare/e-Paper.git ~/e-Paper
pip3 install ~/e-Paper/RaspberryPi_JetsonNano/python/ --break-system-packages

git clone https://github.com/mavotronik/Rpi0w_epaper_clock.git

echo "Ready to RUN!"
echo "Run via [python3 main.py]"
