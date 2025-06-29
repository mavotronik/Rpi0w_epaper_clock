from waveshare_epd import epd2in13_V3
from PIL import Image


class EpaperDisplay:
    def __init__(self, config):
        self.model = config["display"]["model"]
        self.rotate_deg = config["display"]["rotate_deg"]
        self.epd = self._init_driver(self.model)
        self.width = self.epd.width
        self.height = self.epd.height
        self.epd.init()

    def _init_driver(self, model):
        if model == "2in13_V3":
            return epd2in13_V3.EPD()
        else:
            raise ValueError(f"Unsupported display model: {model}")

    def clear(self):
        self.epd.Clear(0xFF)

    def sleep(self):
        self.clear()
        self.epd.sleep()

    def display_image(self, image, partial=True):
        self.epd.init()
        image = image.rotate(self.rotate_deg)
        buffer = self.epd.getbuffer(image)
        if partial:
            self.epd.displayPartial(buffer)
        else:
            self.epd.display(buffer)

    def full_refresh(self):
        self.epd.init()
        self.clear()

    def close(self):
        self.sleep()
