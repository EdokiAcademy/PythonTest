from django.shortcuts import render
from django.http import HttpResponse

import json
import uuid
import time
import hashlib
import base64
import os
import django_heroku
from ecdsa import SigningKey
from ecdsa.util import sigencode_der

def index(request):
    if 'signature' not in request.POST:
        return HttpResponse("Hey, manque une signature en POST");
    else:
        payload = request.POST["signature"]
        with open(os.path.join(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'staticfiles'),"./cert.der"), "rb") as myfile:
            der = myfile.read()
            signing_key = SigningKey.from_der(der)
            signature = signing_key.sign(payload.encode("utf-8"),hashfunc=hashlib.sha256,sigencode=sigencode_der)
            encoded_signature = base64.b64encode(signature)
            encoded_signature = str(encoded_signature, "utf-8")
            return HttpResponse(encoded_signature)

def db(request):
    return render(request, "db.html", {"greetings": ""})
