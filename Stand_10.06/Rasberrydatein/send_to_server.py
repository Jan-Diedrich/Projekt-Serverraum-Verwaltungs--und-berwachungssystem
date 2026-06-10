import requests
import json
import time
import subprocess

RASPI_API_URL = "http://127.0.0.1:5000/data"

SERVER_BENUTZER = "ubuntu"
SERVER_IP_ADRESSE = "2001:7c0:2320:2:f816:3eff:fe40:3b15"
SERVER_ZIELDATEI = "/var/www/serverraumprojekt/daten/sensor_data.json"

while True:
    try:
        api_antwort = requests.get(RASPI_API_URL, timeout=5)

        sensordaten = api_antwort.json()

        with open("/tmp/sensor_data.json", "w") as json_datei:
            json.dump(sensordaten, json_datei)

        subprocess.run([
            "scp",
            "/tmp/sensor_data.json",
            f"{SERVER_BENUTZER}@[{SERVER_IP_ADRESSE}]:{SERVER_ZIELDATEI}"
        ])

        print("Daten gesendet:", sensordaten)

    except Exception as fehler:
        print("Fehler:", fehler)

    time.sleep(5)