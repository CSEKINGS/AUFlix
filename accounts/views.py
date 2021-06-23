from django.shortcuts import render,redirect
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib import auth
from django.http import HttpResponse
from datetime import datetime
import pyrebase
import requests
import json


firebase_config = json.load(open('.'+staticfiles_storage.url("json/config.json")))
firebase = pyrebase.initialize_app(firebase_config['firebase_config'])
authe = firebase.auth()
db=firebase.database()

class Accounts:
    def index(request):
        return render(request,'home.html')
    def dashboard(request):
        return render(request,'dashboard.html')
    def login(request):
        if request.method == 'POST':
            if request.POST.get('submit') == 'signin':
                email = request.POST.get('uname')
                password = request.POST.get('psword')
                try:
                    user = authe.sign_in_with_email_and_password(email,password)
                    # session_id=user['idToken']
                    db.child('users').child(user['localId']).update({'last_login':str(datetime.now())})
                    user_info = db.child('users').child(user['localId']).get().val().items()
                    # print('session:{}'.format(request.session.items))
                    # print('userinfo:{}\ntype:{}'.format(user_info,type(user_info)))
                    for key,value in user_info:
                        request.session[key] = value
                    # request.session['uid']=str(user['localId'])
                    # request.session['email']=str(user['email'])
                    # request.session['name'] = user_info[]
                    # request.session['name']=str(user_info['name'])
                except requests.HTTPError as e:
                    error_json = e.args[1]
                    return HttpResponse("<script>alert('{}!!Please ChecK your Data'); window.location.href = '/accounts/login';</script>".format(json.loads(error_json)['error']['message']))
                return redirect('dashboard')
            elif  request.POST.get('submit') == 'signup':
                email = request.POST.get('email')
                password = request.POST.get('psword')
                name = request.POST.get('name')
                department = request.POST.get('department')
                try:
                    user = authe.create_user_with_email_and_password(email,password)
                    user_data = {
                        "name":name,
                        "userid":user['localId'],
                        "email":email,
                        'department':department,
                        'last_login':'None',
                    }
                    db.child('users').child(user['localId']).set(user_data)
                except requests.HTTPError as e:
                    error_json = e.args[1]
                    return HttpResponse("<script>alert('{}!!Please ChecK your Data'); window.location.href = '/accounts/login';</script>".format(json.loads(error_json)['error']['message']))
                return render(request,'accounts.html')
        return render(request,'accounts.html')
    def logout(request):
        try:
            del request.session['userid']
        except Exception as e:
            pass
        return redirect ('/')
    
    def reset_password(request):
        if request.method == 'POST':
            email =  request.POST.get('uname')
            try:
                li = authe.send_password_reset_email(email)
            except requests.HTTPError as e:
                error_json = e.args[1]
                return HttpResponse("<script>alert('{}!!. ChecK Your Data'); window.location.href = '/accounts/login';</script>".format(json.loads(error_json)['error']['message']))
            return HttpResponse("<script>alert('Your reset link is sended to {}'); window.location.href = '/accounts/login';</script>".format(email))
        return redirect('/accounts/login')