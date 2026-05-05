import requests
import json
import time
import subprocess

RASPI_API = "http://127.0.0.1:5000/data"

SERVER_USER = "ubuntu"
SERVER_IP = "2001:7c0:2320:2:f816:3eff:fe40:3b15"
SERVER_PATH = "/var/www/serverraumprojekt/daten/sensor_data.json"

while True:
    try:
        r = requests.get(RASPI_API, timeout=5)
        daten = r.json()

        with open("/tmp/sensor_data.json", "w") as f:
            json.dump(daten, f)

        subprocess.run([
            "scp",
            "/tmp/sensor_data.json",
            f"{SERVER_USER}@[{SERVER_IP}]:{SERVER_PATH}"
        ])

        print("Daten gesendet:", daten)

    except Exception as e:
        print("Fehler:", e)

    time.sleep(5)