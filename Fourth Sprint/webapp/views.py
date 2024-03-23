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


############################################################################################################################################################
import requests
def usignupactiondef(request):
    
    addr = request.POST['addr']
    email = request.POST['mail']
    pwd = request.POST['pwd']
    ph = request.POST['ph']
    name = request.POST['name']

    d = users.objects.filter(email__exact=email).count()

    if d > 0:
        return render(request, 'signup.html', {'msg': "Email Already Registered"})
    else:

        url = 'http://127.0.0.1:8000/auth/users/'

        payload = {
        'username': name,
        'password': pwd,
        'email': email
        }

        response = requests.post(url, data=payload)

        if response.status_code == 201:

            d = users(name=name, email=email, pwd=pwd,  addr=addr, contact=ph)
            d.save()
            return render(request, 'signup.html', {'msg': "Register Success, You can Login.."})
        
        else:
            return render(request, 'signup.html', {'msg': "Failed to create user. Response: " + response.text})
############################################################################################################################################################

############################################################################################################################################################
def userloginactiondef(request):

    if request.method == 'POST':

        username = request.POST['uid']
        uid = request.POST['mail']
        pwd = request.POST['pwd']

        d = users.objects.filter(email__exact=uid).filter(pwd__exact=pwd).count()

        if d > 0:

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
            return render(request, 'user.html', {'msg': "Login Fail"})

    else:
        return render(request, 'user.html')
############################################################################################################################################################

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

########################################################################################################################################################

def roomadd(request):
    if request.method == 'POST':
    
        roomnum = request.POST['roomnum']
        beds = int(request.POST['beds'])
   

        d = rooms.objects.filter(roomnum__exact=roomnum).count()
        if d > 0:
            d = rooms.objects.all()
            return render(request, 'roomadd.html', {'data':d, 'msg': "Room Already Registered"})
        else:
            d = rooms(roomnum=roomnum, beds=beds,  available=beds)
            d.save()
            d = rooms.objects.all()
            return render(request, 'roomadd.html', {'data':d,'msg': "Room data added !! "})
    else:
        d = rooms.objects.all()
        return render(request, 'roomadd.html',{'data':d})


############################################################################################################################################################

############################################################################################################################################################
from .models import Request

def bookhostel(request):
    if request.method == 'POST':
        email=request.session['useremail'] 
        name=request.session['name'] 
        mode=request.POST['mode']
        d=Request( name=name, email=email, mode=mode, stz='Requested')
        d.save()
        return render(request, 'bookhostel.html',{"msg":'Request forward to hostel management!!'})
    else:
        email=request.session['useremail']
        name=request.session['name']
        d=Request.objects.filter(email=email)
        c=Request.objects.filter(email=email).count()
        b=False
        if c>0:
            b=True
        return render(request, 'bookhostel.html',{"name":name,"email":email,"data":d,"b":b})
############################################################################################################################################################


############################################################################################################################################################
from .models import Request

def newreq(request):
    d=Request.objects.filter(stz='Requested').order_by('-id')
    return render(request, 'viewreq.html',{'data': d})
############################################################################################################################################################


def reject(request, id):
    requests.objects.filter(id = id).update(stz = 'Rejected')
    d=requests.objects.filter(stz='Requested').order_by('-id')
    return render(request, 'viewreq.html',{'data': d, 'msg':'Request Rejected'})

def mbookingpage(request, id):
    d=requests.objects.filter(id=id)
    return render(request, 'mbook.html',{'id': id,'data':d})

import datetime
from django.db.models import F

def mbookingpage2(request):
    from django.db.models import F
    

    dat_e=str(datetime.datetime.now()).split()[0]
    name=request.POST['name']
    email=request.POST['email']
    id=request.POST['id']
    
    room=request.POST['room']
    amt=request.POST['amt']
    d=rooms.objects.filter(roomnum=room).filter(available__gt=0).count()
    print(d,'<<<<<<<<<<<<<<<<')
    if d>0:
        r=requests.objects.filter(id=id)
        s=mbooking(roomnum=room, name=r[0].name, email=r[0].email, dat_e=dat_e, amount=amt)
        s.save()
        d=requests.objects.filter(stz='Requested').order_by('-id')
        requests.objects.filter(id = id).update(stz = 'Accepted')
        s1=transactions(name=name, room=room, email=email, stz='Pay', dat_e=dat_e, amount=amt)
        s1.save()
        rooms.objects.filter(roomnum = room).update(available=F('available')-1)

        return render(request, 'viewreq.html',{'data': d, 'msg':'Request Accepted'})
    else:
        d=requests.objects.filter(stz='Requested').order_by('-id')
        return render(request, 'viewreq.html',{'data': d, 'msg':'Not Available'})
        
   

def dbookingpage(request, id):
    d=requests.objects.filter(id=id)
    return render(request, 'dbook.html',{'id': id,'data':d})


def dbookingpage2(request):

    from .countdays import main
    dat_e=str(datetime.datetime.now()).split()[0]

    name=request.POST['name']
    email=request.POST['email']
    id=request.POST['id']
    dfrom=request.POST['from']
    dto=request.POST['to']
    print(dfrom, dto,'<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    print(main(dfrom, dto),'<<<<<<<<<<<<<<<<')
    days=len(main(dfrom, dto))
    
       
    
    room=request.POST['room']
    amt=int(request.POST['amt'])
    amt=amt*days


    d=rooms.objects.filter(roomnum=room).filter(available__gt=0).count()
    print(d,'<<<<<<<<<<<<<<<<')
    if d>0:
        r=requests.objects.filter(id=id)
        s=dbooking(roomnum=room, name=r[0].name, email=r[0].email, fdate=dfrom, ldate=dto, amount=amt)
        s.save()
        d=requests.objects.filter(stz='Requested').order_by('-id')
        requests.objects.filter(id = id).update(stz = 'Accepted')
        s1=transactions(name=name,  room=room,email=email, stz='Pay', dat_e=dat_e, amount=amt)
        s1.save()
        rooms.objects.filter(roomnum = room).update(available=F('available')-1)

        return render(request, 'viewreq.html',{'data': d, 'msg':'Request Accepted'})
    else:
        d=requests.objects.filter(stz='Requested').order_by('-id')
        return render(request, 'viewreq.html',{'data': d, 'msg':'Not Available'})
        

def booksrd(request):

    from .countdays import main
    dat_e=str(datetime.datetime.now()).split()[0]

    name=request.session['name']
    email=request.session['useremail']

    dfrom=request.POST['d1']
    dto=request.POST['d2']
    print(dfrom, dto,'<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    print(main(dfrom, dto),'<<<<<<<<<<<<<<<<')
    days=len(main(dfrom, dto))

    amt=int(request.POST['amt'])
    amt=amt*days
    s=srbooking( name=name, email=email, dat_e=dat_e, mode="Daily-base: "+dfrom+"-"+dto, amount=amt)
    s.save()
    s1=transactions(name=name,  room='Study Room', email=email, stz='Payed', dat_e=dat_e, amount=amt)
    s1.save()
    return render(request, 'pay2.html',{"amt":amt})

        

def booksrm(request):

    dat_e=str(datetime.datetime.now()).split()[0]

    name=request.session['name']
    email=request.session['useremail']

    
    amt=int(request.POST['amt'])
    s=srbooking( name=name, email=email, dat_e=dat_e, mode="Monthly-base ", amount=amt)
    s.save()
    s1=transactions(name=name,  room='Study Room', email=email, stz='Payed', dat_e=dat_e, amount=amt)
    s1.save()
    return render(request, 'pay2.html',{"amt":amt})
        
def payment(request):
    if request.method == 'POST':
        id=request.POST['id'] 
        amt=request.POST['amt'] 
        transactions.objects.filter(id = id).update(stz = 'Payed')
        return render(request, 'pay.html',{"amt":amt})
    else:
        email=request.session['useremail']
        d=transactions.objects.filter(email=email).filter(stz='Pay')
        return render(request, 'payment.html',{"data":d})

def paymentcomp(request):
    if request.method == 'POST':
        email=request.session['useremail']
        d=transactions.objects.filter(email=email).filter(stz='Pay')
        return render(request, 'payment.html',{"data":d,'msg':'Payment Done!!'})



def transactionsdef(request):
    email=request.session['useremail']
    d=transactions.objects.filter(email=email)
    return render(request, 'transactions.html',{'data':d})

def viewtransactions(request):
    d=transactions.objects.filter(stz='Payed')
    return render(request, 'viewtransactions.html',{'data':d})

def booksr(request):
    email=request.session['useremail']
    name=request.session['name']
    return render(request, 'booksr.html',{'name':name,'email':email})

def paymentcomp2(request):
    if request.method == 'POST':
        return render(request, 'user_home.html',{'msg':'Payment Done!!'})


def missing(request):
    if request.method == 'POST':
        email=request.session['useremail']
        name=request.session['name']
        name_item=request.POST['name_item']
        des=request.POST['des']
        image=request.POST['image']
        ph=request.POST['ph']
        d=missing_items(name=name, email=email, name_item=name_item, description=des, image=image, contact=ph, stz='Active')
        d.save()
        d=missing_items.objects.filter(stz='Active')
        return render(request, 'missing.html',{'msg':'Posted !!', 'data':d})
    else:
        d=missing_items.objects.filter(stz='Active')
        return render(request, 'missing.html',{'data':d})



