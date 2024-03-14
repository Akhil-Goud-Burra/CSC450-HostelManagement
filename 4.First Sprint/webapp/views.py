from django.shortcuts import render, redirect
from django.http import HttpResponse, request

from .models import *

def home(request):
    return render(request, 'index.html')


def userhomedef(request):
    
    if "useremail" in request.session:
        uid = request.session["useremail"]
        d = users.objects.filter(email__exact=uid)
        return render(request, 'user_home.html', {'data': d[0]})

    else:
        return render(request, 'user.html')


def adminhomedef(request):
    if "adminid" in request.session:
        uid = request.session["adminid"]
        return render(request, 'admin_home.html')

    else:
        return render(request, 'admin.html')
    

def userlogoutdef(request):
    try:
        del request.session['useremail']
    except:
        pass
    return render(request, 'user.html')


def adminlogoutdef(request):
    try:
        del request.session['adminid']
    except:
        pass
    return render(request, 'admin.html')


def adminlogindef(request):
    return render(request, 'admin.html')


def userlogindef(request):
    return render(request, 'user.html')


def signupdef(request):
    return render(request, 'signup.html')

############################################################################################################################################
import requests

def usignupactiondef(request):
    addr = request.POST['addr']
    email = request.POST['mail']
    pwd = request.POST['pwd']
    ph = request.POST['ph']
    name = request.POST['name']

    url = 'http://127.0.0.1:8000/auth/users/'

    payload = {
        'username': name,
        'password': pwd,
        'email': email
    }

    # Send a POST request to the specified URL with the data payload
    response = requests.post(url, data=payload)

    # Check if the response is successful
    if response.status_code == 201:
        d = users(name=name, email=email, pwd=pwd,  addr=addr, contact=ph)
        d.save()
        return render(request, 'signup.html', {'msg': "User created successfully! Response: " + response.text})
    else:
        return render(request, 'signup.html', {'msg': "Failed to create user. Response: " + response.text})
##############################################################################################################################################################################
def userloginactiondef(request):

    if request.method == 'POST':
        
        username = request.POST['uid']
        uid = request.POST['mail']
        pwd = request.POST['pwd']

        d = users.objects.filter(email__exact=uid).filter(pwd__exact=pwd).count()

        token_url = 'http://127.0.0.1:8000/api/api-token-auth/'
        token_payload = {
            'username': username,
            'password': pwd
        }

        token_response = requests.post(token_url, data=token_payload)
            
        if token_response.status_code == 200:

            token = token_response.json().get('token')

            auth_url = 'http://127.0.0.1:8000/api/end-user-auth/'
            headers = {'Authorization': f'Token {token}'}

            auth_response = requests.get(auth_url, headers=headers)

            if auth_response.status_code == 200:

                    d = users.objects.filter(email__exact=uid)

                    request.session['useremail'] = uid
                    request.session['name'] = d[0].name
                    return render(request, 'user_home.html', {'data': d[0]})

            else:
                authentication_data = auth_response.json()
                return render(request, 'user.html', {'msg': "Authentication Failed. Error: " + str(authentication_data)})

        else:
            token_data = token_response.json()
            return render(request, 'user.html', {'msg': "Token Retrieval Failed. Error: " + str(token_data)})

    else:
        return render(request, 'user.html') 
##########################################################################################################################################################################################    
def adminloginactiondef(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        pwd = request.POST.get('pwd')

        token_url = 'http://127.0.0.1:8000/api/api-token-auth/'
        token_payload = {
            'username': uid,
            'password': pwd
        }

        token_response = requests.post(token_url, data=token_payload)

        if token_response.status_code == 200:
            token = token_response.json().get('token')

            auth_url = 'http://127.0.0.1:8000/api/admin-user-auth/'
            headers = {'Authorization': f'Token {token}'}

            auth_response = requests.get(auth_url, headers=headers)

            if auth_response.status_code == 200:
                request.session['token'] = token
                return render(request, 'admin_home.html')
            else:
                authentication_data = auth_response.json()
                return render(request, 'admin.html', {'msg': "Authentication Failed. Error: " + str(authentication_data)})
        else:
            token_data = token_response.json()
            return render(request, 'admin.html', {'msg': "Token Retrieval Failed. Error: " + str(token_data)})
    else:
        return render(request, 'admin.html')
########################################################################################################################################################