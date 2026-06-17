import json
import os
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt



SENSOR_DATEI = "/var/www/serverraumprojekt/daten/sensor_data.json"
TUER_DATEI = "/var/www/serverraumprojekt/daten/tuer_data.json"


# JAN
def startseite(request):

    return render(request, "index.html")


# JAN
@csrf_exempt
def sensordaten_api(request):

    if request.method == "POST":

        daten = json.loads(request.body)

        with open(SENSOR_DATEI, "w", encoding="utf-8") as datei:
            json.dump(daten, datei, ensure_ascii=False)

        print("Sensordaten empfangen:", daten)

        return JsonResponse({
            "success": True
        })


    if request.method == "GET":

        with open(SENSOR_DATEI, "r", encoding="utf-8") as datei:
            daten = json.load(datei)


        # TOBI
        if os.path.exists(TUER_DATEI):

            with open(TUER_DATEI, "r", encoding="utf-8") as datei:
                tuer = json.load(datei)

            daten["tuer_offen"] = tuer.get("tuer_offen", False)
            daten["letzter_zugriff"] = tuer.get("letzter_zugriff", "—")

        else:

            daten["tuer_offen"] = False
            daten["letzter_zugriff"] = "Keine Daten"


        # JAN
        return JsonResponse(daten)


    return JsonResponse({
        "success": False
    })


# TOBI
@csrf_exempt
def tuerstatus_api(request):

    if request.method == "POST":

        daten = json.loads(request.body)

        with open(TUER_DATEI, "w", encoding="utf-8") as datei:
            json.dump(daten, datei, ensure_ascii=False)

        return JsonResponse({
            "success": True
        })


    return JsonResponse({
        "success": False
    })