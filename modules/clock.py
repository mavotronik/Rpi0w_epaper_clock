import datetime

def render(draw, fonts, config):
    now = datetime.datetime.now()

    time_format = config.get("time_format", "%H:%M")
    date_format = config.get("date_format", "%d.%m.%Y")

    time_str = now.strftime(time_format)
    date_str = now.strftime(date_format)

    clock_pos = config.get("clock_pos", (60, 25))
    date_pos = config.get("date_pos", (75, 65))

    draw.text(clock_pos, time_str, font=fonts["time"], fill=0)
    draw.text(date_pos, date_str, font=fonts["date"], fill=0)
