from waveshare_epd import epd2in13_V3
import time
import datetime
import os
import PIL
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import psutil
import socket

RES_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources/')

FONT = os.path.join(RES_DIR, 'FreeMono.ttf')
FONTBOLD = os.path.join(RES_DIR, 'FreeMonoBold.ttf')

resfont_size = 13
resfont = ImageFont.truetype(FONT, resfont_size)
try:

    epd = epd2in13_V3.EPD()
    epd.init()
    #epd.Clear(0xFF)
    
    cpu_ = psutil.cpu_percent()
    mem_ = psutil.virtual_memory()
    cpu = "CPU:" + str(cpu_) + "%"
    mem = "RAM:" + str(mem_.percent)+ "%"
    
    image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(image)
    draw.line([(0,20),(250,20)], fill = 0,width = 3)
    draw.line([(0,105),(250,105)], fill = 0,width = 3)
    draw.text((5, 111), cpu, font = resfont, fill = 0)
    draw.text((170, 111), mem, font = resfont, fill = 0)
    
    epd.display(epd.getbuffer(image))
    
    ifaddresses = [ifname+' '+str(ip.address) for ifname in psutil.net_if_addrs().keys() for ip in psutil.net_if_addrs()[ifname] if ip.family == socket.AF_INET]
    netstring = '\n'.join(ifaddresses)
    print(netstring)

    
    epd2in13_V3.epdconfig.module_exit()

except IOError as e:
    print(e)

except KeyboardInterrupt:
    print("ctrl + c:")
    epd2in13_V3.epdconfig.module_exit()
    exit()
