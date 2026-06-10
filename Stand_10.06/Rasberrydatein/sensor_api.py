from flask import Flask, jsonify
from flask_cors import CORS
import board
import adafruit_dht
import RPi.GPIO as GPIO
import time

sensor_api = Flask(__name__)
CORS(sensor_api)


temperatur_sensor = adafruit_dht.DHT11(board.D4)


LUEFTER_GPIO_PIN = 17
TEMPERATUR_GRENZWERT = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(LUEFTER_GPIO_PIN, GPIO.OUT)
GPIO.output(LUEFTER_GPIO_PIN, GPIO.LOW)

def lese_temperatur_und_luftfeuchtigkeit():

    for versuch in range(3):

        try:

            gemessene_temperatur = temperatur_sensor.temperature
            gemessene_luftfeuchtigkeit = temperatur_sensor.humidity

            if gemessene_temperatur is not None and gemessene_luftfeuchtigkeit is not None:

                return gemessene_temperatur, gemessene_luftfeuchtigkeit

        except RuntimeError:

            time.sleep(2)

    return None, None

@sensor_api.route("/data")
def liefere_sensordaten():

    gemessene_temperatur, gemessene_luftfeuchtigkeit = lese_temperatur_und_luftfeuchtigkeit()

    if gemessene_temperatur is not None:

        if gemessene_temperatur > TEMPERATUR_GRENZWERT:

            GPIO.output(LUEFTER_GPIO_PIN, GPIO.HIGH)

            luefter_status = "AN"

            luefter_grund = "Temperatur Ã¼ber Grenzwert"

        else:

            GPIO.output(LUEFTER_GPIO_PIN, GPIO.LOW)

            luefter_status = "AUS"

            luefter_grund = "Temperatur unter Grenzwert"

    else:

        GPIO.output(LUEFTER_GPIO_PIN, GPIO.LOW)

        luefter_status = "AUS"

        luefter_grund = "Keine gï¿½ltigen Sensordaten"

    return jsonify({

        "temperatur": gemessene_temperatur,

        "luftfeuchtigkeit": gemessene_luftfeuchtigkeit,

        "motor": luefter_status,

        "motor_grund": luefter_grund,

        "grenzwert": TEMPERATUR_GRENZWERT

    })

try:

    sensor_api.run(host="0.0.0.0", port=5000)

finally:

    GPIO.output(LUEFTER_GPIO_PIN, GPIO.LOW)

    GPIO.cleanup()