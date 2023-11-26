from waveshare_epd import epd2in13_V3
import time
import datetime
import os
import PIL
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import psutil

RES_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources/')

DATEFORMAT = "%d/%m/%y"
TIMEFORMAT = "%H:%M:%S"
FONT = os.path.join(RES_DIR, 'FreeMono.ttf')
FONTBOLD = os.path.join(RES_DIR, 'FreeMonoBold.ttf')

timefont_size = 35
timefont = ImageFont.truetype(FONTBOLD, timefont_size)
datefont_size = 15
datefont = ImageFont.truetype(FONTBOLD, datefont_size)
resfont_size = 13
resfont = ImageFont.truetype(FONT, resfont_size)

NumToClear = 0

try:

    epd = epd2in13_V3.EPD()
    epd.init()
    epd.Clear(0xFF)
    
    while True:
        epd.init()
        
        if (NumToClear == 10):
            epd.Clear(0xFF)
            NumToClear = 0  
    
        dt_now = datetime.datetime.now()
        time_rn = dt_now.strftime(TIMEFORMAT)
        date_rn = dt_now.strftime(DATEFORMAT)
        
        cpu_ = psutil.cpu_percent()
        mem_ = psutil.virtual_memory()
        cpu = "CPU:" + str(cpu_) + "%"
        mem = "RAM:" + str(mem_.percent)+ "%"

        image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(image)
        draw.line([(0,20),(250,20)], fill = 0,width = 3)
        draw.line([(0,105),(250,105)], fill = 0,width = 3)
        

        draw.text((25, 25), time_rn, font = timefont, fill = 0)
        draw.text((75, 65), date_rn, font = datefont, fill = 0)
        
        draw.text((5, 111), cpu, font = resfont, fill = 0)
        draw.text((170, 111), mem, font = resfont, fill = 0)
        
        epd.displayPartial(epd.getbuffer(image))
    
        epd.Clear(0xFF)
        epd.sleep()
        NumToClear = NumToClear + 1
        print(f"NumToClear:", NumToClear)
        
        time.sleep(60)


except IOError as e:
    print(e)

except KeyboardInterrupt:
    print("ctrl + c:")
    epd2in13_V3.epdconfig.module_exit()
    exit()
