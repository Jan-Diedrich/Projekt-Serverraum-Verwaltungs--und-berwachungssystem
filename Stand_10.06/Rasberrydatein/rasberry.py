import json
import time
import subprocess
import board
import adafruit_dht
import RPi.GPIO as GPIO


SERVER_BENUTZER = "ubuntu"
SERVER_IP_ADRESSE = "2001:7c0:2320:2:f816:3eff:fe40:3b15"
SERVER_ZIELDATEI = "/var/www/serverraumprojekt/daten/sensor_data.json"

LOKALE_JSON_DATEI = "/tmp/sensor_data.json"

LUEFTER_PIN = 17
TEMPERATUR_GRENZWERT = 18

sensor = adafruit_dht.DHT11(board.D4)

GPIO.setmode(GPIO.BCM)
GPIO.setup(LUEFTER_PIN, GPIO.OUT)
GPIO.output(LUEFTER_PIN, GPIO.LOW)


def lese_sensorwerte():
    for versuch in range(3):
        try:
            temperatur = sensor.temperature
            luftfeuchtigkeit = sensor.humidity

            if temperatur is not None and luftfeuchtigkeit is not None:
                return temperatur, luftfeuchtigkeit

        except RuntimeError:
            time.sleep(2)

    return None, None


def steuere_luefter(temperatur):
    if temperatur is None:
        GPIO.output(LUEFTER_PIN, GPIO.LOW)
        return "AUS", "Keine gültigen Sensordaten"

    if temperatur > TEMPERATUR_GRENZWERT:
        GPIO.output(LUEFTER_PIN, GPIO.HIGH)
        return "AN", "Temperatur über Grenzwert"

    GPIO.output(LUEFTER_PIN, GPIO.LOW)
    return "AUS", "Temperatur unter Grenzwert"


def erstelle_sensordaten():
    temperatur, luftfeuchtigkeit = lese_sensorwerte()

    luefter_status, luefter_grund = steuere_luefter(temperatur)

    daten = {
        "temperatur": temperatur,
        "luftfeuchtigkeit": luftfeuchtigkeit,
        "motor": luefter_status,
        "motor_grund": luefter_grund,
        "grenzwert": TEMPERATUR_GRENZWERT
    }

    return daten


def speichere_json_datei(daten):
    with open(LOKALE_JSON_DATEI, "w", encoding="utf-8") as datei:
        json.dump(daten, datei, ensure_ascii=False)


def sende_datei_an_server():
    subprocess.run([
        "scp",
        LOKALE_JSON_DATEI,
        f"{SERVER_BENUTZER}@[{SERVER_IP_ADRESSE}]:{SERVER_ZIELDATEI}"
    ])


try:
    while True:
        sensordaten = erstelle_sensordaten()

        speichere_json_datei(sensordaten)

        sende_datei_an_server()

        print("Daten gesendet:", sensordaten)

        time.sleep(5)

except KeyboardInterrupt:
    print("Programm beendet")

finally:
    GPIO.output(LUEFTER_PIN, GPIO.LOW)
    GPIO.cleanup()