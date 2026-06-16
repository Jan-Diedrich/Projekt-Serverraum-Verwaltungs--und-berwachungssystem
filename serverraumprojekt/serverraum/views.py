import json
import os
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


SENSOR_DATEI = "/var/www/serverraumprojekt/daten/sensor_data.json"
TUER_DATEI   = "/var/www/serverraumprojekt/daten/tuer_data.json"


def startseite(request):
    return render(request, "index.html")


@csrf_exempt
def sensordaten_api(request):
    """Luefter-Pi: Temperatur, Luftfeuchtigkeit, Motor"""

    if request.method == "POST":
        daten = json.loads(request.body)
        with open(SENSOR_DATEI, "w", encoding="utf-8") as f:
            json.dump(daten, f, ensure_ascii=False)
        return JsonResponse({"success": True})

    if request.method == "GET":
        # Sensordaten laden
        with open(SENSOR_DATEI, "r", encoding="utf-8") as f:
            daten = json.load(f)

        # Türdaten dazuladen (falls vorhanden)
        if os.path.exists(TUER_DATEI):
            with open(TUER_DATEI, "r", encoding="utf-8") as f:
                tuer = json.load(f)
            daten["tuer_offen"]      = tuer.get("tuer_offen", False)
            daten["letzter_zugriff"] = tuer.get("letzter_zugriff", "")
        else:
            daten["tuer_offen"]      = False
            daten["letzter_zugriff"] = "Keine Daten"

        return JsonResponse(daten)

    return JsonResponse({"success": False})


@csrf_exempt
def tuerstatus_api(request):
    """Tuer-Pi: RFID-Status und Tuerzustand"""

    if request.method == "POST":
        daten = json.loads(request.body)
        with open(TUER_DATEI, "w", encoding="utf-8") as f:
            json.dump(daten, f, ensure_ascii=False)
        return JsonResponse({"success": True})

    return JsonResponse({"success": False})