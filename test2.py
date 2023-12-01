import requests

HA_IP = "192.168.2.12:8123"
HA_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI0MDFiZTZmMGY0M2Q0ODUxOGUwYTJjYzE0NmI4MTZhNiIsImlhdCI6MTcwMTM3MjE5OCwiZXhwIjoyMDE2NzMyMTk4fQ.pulxx0mfuLPTRxHj5A6P4D4EjO-v3LBiInuWUZZNTD4"

url = f"http://{HA_IP}/api/states/sensor.datchik_za_oknom_temperature"
headers = {
    "Authorization": f"Bearer {HA_TOKEN}",
    "content-type": "application/json",
}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    state_value = data['state']
    print("State value:", state_value)
else:
    print("Failed to fetch data:", response.status_code)