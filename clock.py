from waveshare_epd import epd2in13_V3
import time
import datetime
import os
import PIL
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

RES_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources/')

DATEFORMAT = "%d/%m/%y"
TIMEFORMAT = "%H:%M:%S"
FONT = os.path.join(RES_DIR, 'FreeMono.ttf')
FONTBOLD = os.path.join(RES_DIR, 'FreeMonoBold.ttf')

timefont_size = 35
timefont = ImageFont.truetype(FONTBOLD, timefont_size)

NumToClear = 0

try:

    epd = epd2in13_V3.EPD()
    epd.init()
    
    
    while True:
        epd.init()
        
        if (NumToClear == 5):
            epd.Clear(0xFF)
            NumToClear = 0  
    
        dt_now = datetime.datetime.now()
        time_rn = dt_now.strftime(TIMEFORMAT)
        date_rn = dt_now.strftime(DATEFORMAT)

        image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(image)
        # draw = draw.transpose(Image.ROTATE_180)
        draw.text((40, 15), time_rn, font = timefont, fill = 0)
        draw.text((20, 60), date_rn, font = timefont, fill = 0)
        epd.displayPartial(epd.getbuffer(image))
    
        epd.Clear(0xFF)
        epd.sleep()
        NumToClear = NumToClear + 1
        print(f"NumToClear:", NumToClear)
        
        time.sleep(10)


except IOError as e:
    print(e)

except KeyboardInterrupt:
    print("ctrl + c:")
    epd2in13_V3.epdconfig.module_exit()
    exit()
