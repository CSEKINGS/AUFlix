from django.shortcuts import render,redirect
from django.contrib.staticfiles.storage import staticfiles_storage
from datetime import datetime
from videopage.scrap import AUSCRAPER
import pyrebase
import json


firebase_config = json.load(open('.'+staticfiles_storage.url("json/config.json")))
firebase = pyrebase.initialize_app(firebase_config['firebase_config'])
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