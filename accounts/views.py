from django.shortcuts import render,redirect
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib import auth
from django.http import HttpResponse
import pyrebase
import requests

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
database=firebase.database()

class Accounts:
    def index(request):
        return render(request,'home.html')
    def dashboard(request):
        # if request.session['uid']
        return render(request,'dashboard.html')
    def login(request):
        if request.method == 'POST':
            if request.POST.get('submit') == 'signin':
                email = request.POST.get('uname')
                password = request.POST.get('psword')
                try:
                    user = authe.sign_in_with_email_and_password(email,password)
                    session_id=user['idToken']
                    request.session['uid']=str(session_id)
                except Exception as e:
                    print(e)
                    return HttpResponse("<script>alert('Invalid Credentials!!Please ChecK your Data'); window.location.href = '/login';</script>")
                print(user)
                return redirect('dashboard')
                # return render(request,'home.html')
            elif  request.POST.get('submit') == 'signup':
                email = request.POST.get('email')
                password = request.POST.get('psword')
                name = request.POST.get('name')
                print('{}\n{}\n{}'.format(email,password,name))
                try:
                    user = authe.create_user_with_email_and_password(email,password)
                    uid = user['localId']
                    idtoken = request.session['uid']
                except requests.exceptions.HTTPError as error:
                    print(error)
                    return HttpResponse("<script>alert('Something Went wrong! Please Try again later.'); window.location.href = '/login';</script>")
                return render(request,'login.html')
        return render(request,'accounts.html')
    def logout(request):
        try:
            del request.session['uid']
        except Exception as e:
            print(e)
            pass
        return redirect ('/login')
    
    def reset_password(request):
        if request.method == 'POST':
            email =  request.POST.get('uname')
            print(email)
            try:
                li = authe.send_password_reset_email(email)
                print(li)
            except Exception as e:
                print(e)
                return HttpResponse("<script>alert('Your email is not registered'); window.location.href = '/login';</script>")
            return HttpResponse("<script>alert('Your reset link is sended to {}'); window.location.href = '/login';</script>".format(email))
        return redirect('/login')