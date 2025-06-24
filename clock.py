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

RES_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources/')    # directory with fonts, pictures, etc...

DATEFORMAT = "%d/%m/%y"
TIMEFORMAT = "%H:%M"

FONT = os.path.join(RES_DIR, 'FreeMono.ttf')
FONTBOLD = os.path.join(RES_DIR, 'FreeMonoBold.ttf')    # fonts

HA_IP = "your homeassistant ip:8123"
HA_TOKEN = "your long live homeassistant token"

timefont_size = 35
timefont = ImageFont.truetype(FONTBOLD, timefont_size)    # font for display time

datefont_size = 15
datefont = ImageFont.truetype(FONTBOLD, datefont_size)    # font for display date

resfont_size = 13
resfont = ImageFont.truetype(FONT, resfont_size)    # font for display system resources

NumToClear = 0



url = f"http://{HA_IP}/api/states/sensor.datchik_za_oknom_temperature"
headers = {
    "Authorization": f"Bearer {HA_TOKEN}",
    "content-type": "application/json",
}

try:

    epd = epd2in13_V3.EPD()
    epd.init()    # initial display
    epd.Clear(0xFF)    # clear display
    
    while True:
        epd.init()    # initial display again after sleeping
        
        if (NumToClear == 30):    # numbers of display partial updates to do full update
            epd.Clear(0xFF)
            NumToClear = 0  
    
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            out_temp_value = data['state']
            #print("State value:", state_value)
        else:
            print("Failed to fetch data:", response.status_code)
    
        dt_now = datetime.datetime.now()
        seconds_until_next_minute = 60 - dt_now.time().second    # calculate secons until next minute
        time_rn = dt_now.strftime(TIMEFORMAT)
        date_rn = dt_now.strftime(DATEFORMAT)    # convert date and time to readable format
        
        cpu_ = psutil.cpu_percent()
        mem_ = psutil.virtual_memory()
        cpu = "CPU:" + str(cpu_) + "%"
        mem = "RAM:" + str(mem_.percent)+ "%"     
        out_temp_value_str = "Ул. температура: "+out_temp_value+" °C"    # create string to send to display

        image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(image)
        draw.line([(0,20),(250,20)], fill = 0,width = 3)    # draw upper line
        draw.line([(0,105),(250,105)], fill = 0,width = 3)    # draw lower line
        

        draw.text((60, 25), time_rn, font = timefont, fill = 0)    # display time
        draw.text((75, 65), date_rn, font = datefont, fill = 0)    # display date
        draw.text((10, 80), out_temp_value_str, font = resfont, fill = 0)    # display outdoor temp
        
        draw.text((55, 3), "192.168.2.167", font = resfont, fill = 0)    # display text
        draw.text((5, 111), cpu, font = resfont, fill = 0)    # display cpu usage
        draw.text((170, 111), mem, font = resfont, fill = 0)    # display ram usage
        
        epd.displayPartial(epd.getbuffer(image))
    
        epd.Clear(0xFF)
        epd.sleep()     # sleep, eco mode
        NumToClear = NumToClear + 1
        print(f"NumToClear:", NumToClear)
        
        time.sleep(seconds_until_next_minute)     # wait for the next minute


except IOError as e:
    print(e)

except KeyboardInterrupt:
    print("ctrl + c:")
    epd2in13_V3.epdconfig.module_exit()
    exit()
