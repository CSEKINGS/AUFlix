from django.shortcuts import render
import pyrebase


firebaseConfig = {
    "apiKey": "AIzaSyB2jAveBDZ6m8YBKEh1iCP2xJLLSeFoYyA",
  "authDomain": "auflix-67633.firebaseapp.com",
  "projectId": "auflix-67633",
  "storageBucket": "auflix-67633.appspot.com",
  "messagingSenderId": "757795130164",
  "appId": "1:757795130164:web:d2dd6d191911a0a7977361",
  "databaseURL": "https://auflix-67633-default-rtdb.firebaseio.com/",
        }
firebase = pyrebase.initialize_app(firebaseConfig)
authe = firebase.auth()
db=firebase.database()

# Create your views here.
class Videopage:
    def videos(request):
        return render(request,'videos.html',{'context':db.child('test').get().val().items()})