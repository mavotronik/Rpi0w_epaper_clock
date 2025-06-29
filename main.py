import time
import datetime
import os
from PIL import Image, ImageFont, ImageDraw
import psutil
import yaml
import importlib

from display import EpaperDisplay


# Пути к ресурсам
RES_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources/')
FONT = os.path.join(RES_DIR, 'FreeMono.ttf')
FONTBOLD = os.path.join(RES_DIR, 'FreeMonoBold.ttf')

# Шрифты
timefont_size = 35
datefont_size = 15
resfont_size = 13

fonts = {
    "time": ImageFont.truetype(FONTBOLD, timefont_size),
    "date": ImageFont.truetype(FONTBOLD, datefont_size),
    "res": ImageFont.truetype(FONT, resfont_size),
}

def load_config(file_path="config.yaml"):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)
    
# Модули
def load_modules(module_names):
    modules = []
    for name in module_names:
        try:
            mod = importlib.import_module(f"modules.{name}")
            modules.append(mod)
        except Exception as e:
            print(f"Failed to load module '{name}': {e}")
    return modules

def image_build(cpu, mem, fonts, width, height, config, modules):
    
    resfont = fonts["res"]

    image = Image.new('1', (height, width), 255)
    draw = ImageDraw.Draw(image)

    draw.line([(0, 20), (250, 20)], fill=0, width=3)
    draw.line([(0, 105), (250, 105)], fill=0, width=3)
    draw.text((5, 111), cpu, font=resfont, fill=0)
    draw.text((170, 111), mem, font=resfont, fill=0)

    for module in modules:
        module_config = config.get(module.__name__.split('.')[-1], {})
        try:
            module.render(draw, fonts, module_config)
        except Exception as e:
            print(f"Error in module '{module.__name__}': {e}")

    return image

def main():

    config = load_config()
    modules = load_modules(config.get("modules", []))
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

        cpu = f"CPU:{psutil.cpu_percent()}%"
        mem = f"RAM:{psutil.virtual_memory().percent}%"

        image = image_build(cpu, mem, fonts, display.width, display.height, config, modules)

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
