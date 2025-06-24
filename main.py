from waveshare_epd import epd2in13_V3
import time
import datetime
import os
import PIL
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import psutil
import requests
import yaml

RES_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources/')    # directory with fonts, pictures, etc...

FONT = os.path.join(RES_DIR, 'FreeMono.ttf')
FONTBOLD = os.path.join(RES_DIR, 'FreeMonoBold.ttf') # fonts

timefont_size = 35
timefont = ImageFont.truetype(FONTBOLD, timefont_size)    # font for display time

datefont_size = 15
datefont = ImageFont.truetype(FONTBOLD, datefont_size)    # font for display date

resfont_size = 13
resfont = ImageFont.truetype(FONT, resfont_size)    # font for display system resources

fonts = timefont, datefont, resfont

def load_config(file_path="config.yaml"):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)

def init_display():
    epd = epd2in13_V3.EPD()
    epd.init()
    epd.Clear(0xFF)
    return epd

def update_display(epd, image):
    epd.displayPartial(epd.getbuffer(image))

def sleep_display(epd):
    epd.Clear(0xFF)
    epd.sleep()


def image_build(time, date, cpu, mem, fonts, epd, rotate_deg):
    timefont, datefont, resfont = fonts
    image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(image)
    draw.line([(0,20),(250,20)], fill = 0,width = 3)    # draw upper line
    draw.line([(0,105),(250,105)], fill = 0,width = 3)    # draw lower line

    draw.text((60, 25), time, font = timefont, fill = 0)    # display time
    draw.text((75, 65), date, font = datefont, fill = 0)    # display date
    draw.text((5, 111), cpu, font = resfont, fill = 0)    # display cpu usage
    draw.text((170, 111), mem, font = resfont, fill = 0)    # display ram usage

    return image.rotate(rotate_deg)
    

def main():
    config = load_config()
    DATEFORMAT = config["date"]["format"]
    TIMEFORMAT = config["time"]["format"]
    full_clear_after = config["display"]["full_clear_after"]
    rotate_deg = config["display"]["rotate_deg"]
    epd = init_display()
    NumToClear = 0
    

    while True:
        if (NumToClear == full_clear_after):    # numbers of display partial updates to do full update
            epd.Clear(0xFF)
            NumToClear = 0
        
        dt_now = datetime.datetime.now()
        seconds_until_next_minute = 60 - dt_now.second
        time_rn = dt_now.strftime(TIMEFORMAT)
        date_rn = dt_now.strftime(DATEFORMAT)

        cpu_ = psutil.cpu_percent()
        mem_ = psutil.virtual_memory()
        cpu = "CPU:" + str(cpu_) + "%"
        mem = "RAM:" + str(mem_.percent) + "%"

        image = image_build(time_rn, date_rn, cpu, mem, fonts, epd, rotate_deg)
        update_display(epd, image)
        NumToClear = NumToClear + 1
        print(NumToClear)
        time.sleep(seconds_until_next_minute)
        
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Error:")
        print(e)
