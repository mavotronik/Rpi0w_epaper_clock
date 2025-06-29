# Rpi0w_epaper_clock
---

![Clock photo](https://github.com/mavotronik/Rpi0w_epaper_clock/blob/main/photo_clock.jpg?raw=true "Image of the clock")

---
# About:
## Rpi0w epaper clock is a project of the clock based on Raspberry Pi Zero W and Waveshave V3 2.13 inch epaper display. 
### It can display:
- Time
- Date

# How to install:
1. Turn on SPI via ```sudo raspi-config```
    ``` 
    Interfacing Options -> SPI
    ```
2. Install dependencies:
    ```
    sudo apt update
    sudo apt install git  python3-pip python3-numpy python3-pillow -y
    pip3 install RPi.GPIO spidev --break-system-packages
    ```
3. Install dependencies for epaper diasplays:
    ```
    git clone https://github.com/waveshare/e-Paper.git ~/e-Paper
    pip3 install ~/e-Paper/RaspberryPi_JetsonNano/python/ --break-system-packages
    ```
4. Download source code: 
    ```
    git clone https://github.com/mavotronik/Rpi0w_epaper_clock.git
    ```
5. Run it:
    ```
    python3 main.py
    ```