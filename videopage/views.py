from django.shortcuts import render,redirect
from django.contrib.staticfiles.storage import staticfiles_storage
from datetime import datetime
from videopage.scrap import AUSCRAPER
from dotenv import load_dotenv
import pyrebase
import json
import os

load_dotenv()
firebase = pyrebase.initialize_app({
        "apiKey": os.environ.get("API_KEY"),
        "authDomain": os.environ.get("AUTH_DOMAIN"),
        "projectId": os.environ.get("PROJECTID"),
        "storageBucket": os.environ.get("STORAGE_BUCKET"),
        "messagingSenderId": os.environ.get("SENDERID"),
        "appId": os.environ.get("APP_ID"),
        "databaseURL": os.environ.get("DB_URL")
        })
authe = firebase.auth()
db=firebase.database()


# Create your views here.
class Videopage:
    def videos(request):
        return render(request,'videos.html',{'videos':db.child('videos').get().val().items(),'notes':db.child('notes').get().val().items()})

    def scrap(request):
        AS=AUSCRAPER()
        print(abs(int(datetime.now().strftime('%j'))-int(AS.db.child('vdate').get().val())))
        if abs(int(datetime.now().strftime('%j'))-int(AS.db.child('vdate').get().val())) >= 7 :
            AS.Yscrap()
            AS.Nscrap()
            AS.db.child('vdate').set(int(datetime.now().strftime('%j')))
        return redirect('videos')