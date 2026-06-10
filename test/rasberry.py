import time  
import requests  
import board  
import adafruit_dht  
import RPi.GPIO as GPIO  

SERVER_URL = "http://[2001:7c0:2320:2:f816:3eff:fe40:3b15]/api/sensordaten/"  

LUEFTER_PIN = 17  
TEMPERATUR_GRENZWERT = 18  

sensor = adafruit_dht.DHT11(board.D4)  

GPIO.setmode(GPIO.BCM)  # BCM-Pin-Nummern verwenden
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
        return "AUS", "Keine gÃ¼ltigen Sensordaten"

    if temperatur > TEMPERATUR_GRENZWERT:
        GPIO.output(LUEFTER_PIN, GPIO.HIGH)
        return "AN", "Temperatur Ã¼ber Grenzwert"

    GPIO.output(LUEFTER_PIN, GPIO.LOW)
    return "AUS", "Temperatur unter Grenzwert"


def erstelle_daten():
    temperatur, luftfeuchtigkeit = lese_sensorwerte()
    luefter_status, luefter_grund = steuere_luefter(temperatur)

    return {
        "temperatur": temperatur,
        "luftfeuchtigkeit": luftfeuchtigkeit,
        "motor": luefter_status,
        "motor_grund": luefter_grund,
        "grenzwert": TEMPERATUR_GRENZWERT
    }


try:
    while True:
        daten = erstelle_daten()

        antwort = requests.post(SERVER_URL, json=daten, timeout=5)

        print("Gesendet:", daten)
        print("Serverantwort:", antwort.status_code)

        time.sleep(5)

except KeyboardInterrupt:
    print("Programm beendet")

finally:
    GPIO.output(LUEFTER_PIN, GPIO.LOW)
    GPIO.cleanup()