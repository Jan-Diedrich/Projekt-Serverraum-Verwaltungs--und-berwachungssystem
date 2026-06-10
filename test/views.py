import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


SENSOR_DATEI = "/var/www/serverraumprojekt/daten/sensor_data.json"


def startseite(request):

    return render(request, "index.html")


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

        return JsonResponse(daten)


    return JsonResponse({
        "success": False
    })