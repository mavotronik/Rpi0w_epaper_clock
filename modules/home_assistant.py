import requests
import json

def render(draw, fonts, config):

    ip = config.get("ip")
    token = config.get("token")
    entity = config.get("entity")
    pos = config.get("pos", (60, 25))

    headers = {
            "Authorization": f"Bearer {token}",
            "content-type": "application/json",
        }

    url = f"{ip}/api/states/{entity}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        value = data.get("state", "N/A")
    else: value = "N/D"

    draw.text(pos, value, font=fonts["res"], fill=0)

