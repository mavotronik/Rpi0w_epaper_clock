from waveshare_epd import epd2in13_V3
import time

try:

    epd = epd2in13_V3.EPD()
    epd.init()
    epd.Clear(0xFF)
    epd2in13_V3.epdconfig.module_exit()

except IOError as e:
    print(e)

except KeyboardInterrupt:
    print("ctrl + c:")
    epd2in13_V3.epdconfig.module_exit()
    exit()
