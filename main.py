import time
import datetime
import os
from PIL import Image, ImageFont, ImageDraw
import psutil
import yaml

from display import EpaperDisplay

# Пути к ресурсам
RES_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources/')
FONT = os.path.join(RES_DIR, 'FreeMono.ttf')
FONTBOLD = os.path.join(RES_DIR, 'FreeMonoBold.ttf')

# Шрифты
timefont_size = 35
datefont_size = 15
resfont_size = 13

timefont = ImageFont.truetype(FONTBOLD, timefont_size)
datefont = ImageFont.truetype(FONTBOLD, datefont_size)
resfont = ImageFont.truetype(FONT, resfont_size)
fonts = timefont, datefont, resfont

def load_config(file_path="config.yaml"):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)

def image_build(time, date, cpu, mem, fonts, width, height):
    timefont, datefont, resfont = fonts
    image = Image.new('1', (height, width), 255)
    draw = ImageDraw.Draw(image)

    draw.line([(0, 20), (250, 20)], fill=0, width=3)
    draw.line([(0, 105), (250, 105)], fill=0, width=3)

    draw.text((60, 25), time, font=timefont, fill=0)
    draw.text((75, 65), date, font=datefont, fill=0)
    draw.text((5, 111), cpu, font=resfont, fill=0)
    draw.text((170, 111), mem, font=resfont, fill=0)

    return image

def main():
    config = load_config()
    DATEFORMAT = config["date"]["format"]
    TIMEFORMAT = config["time"]["format"]
    full_clear_after = config["display"]["full_clear_after"]

    display = EpaperDisplay(config)
    NumToClear = 0
    display.full_refresh()

    while True:
        if NumToClear == full_clear_after:
            display.full_refresh()
            NumToClear = 0
            print("[Display] Full cleared")

        dt_now = datetime.datetime.now()
        seconds_until_next_minute = 60 - dt_now.second
        time_rn = dt_now.strftime(TIMEFORMAT)
        date_rn = dt_now.strftime(DATEFORMAT)

        cpu = f"CPU:{psutil.cpu_percent()}%"
        mem = f"RAM:{psutil.virtual_memory().percent}%"

        image = image_build(time_rn, date_rn, cpu, mem, fonts, display.width, display.height)
        display.display_image(image, partial=True)
        display.sleep()
        NumToClear += 1

        print(f"[Display] Updated: {NumToClear}")
        time.sleep(seconds_until_next_minute)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Error:")
        print(e)
