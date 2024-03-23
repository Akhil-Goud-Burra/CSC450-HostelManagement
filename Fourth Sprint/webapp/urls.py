"""WebC URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [ 
    path('', views.home, name="Welcome"), 
    path('alogin/', views.adminlogindef, name="adminlogindef"), 
    path('ulogin/', views.userlogindef, name="userlogindef"),    
    path('userreg/', views.signupdef, name="signupdef"),    
    path('usignupaction/', views.usignupactiondef, name="usignupactiondef"),
    path('userloginaction/', views.userloginactiondef, name="userloginactiondef"),
    path('userhome/', views.userhomedef, name="userhome"),
    path('userlogout/', views.userlogoutdef, name="userlogout"),
    path('adminloginaction/', views.adminloginactiondef, name="adminloginactiondef"),
    path('adminhome/', views.adminhomedef, name="adminhome"),
    path('adminlogout/', views.adminlogoutdef, name="adminlogout"),
    path('roomadd/', views.roomadd, name="roomadd"),
    path('bookhostel/', views.bookhostel, name="bookhostel"),
    path('newreq/', views.newreq, name="newreq"),
    path('reject/<str:id>/', views.reject, name="reject"),
    path('mbookingpage/<str:id>/', views.mbookingpage, name="mbookingpage"),
    path('dbookingpage/<str:id>/', views.dbookingpage, name="dbookingpage"),
    path('mbookingpage2/', views.mbookingpage2, name="mbookingpage2"),
    path('dbookingpage2/', views.dbookingpage2, name="dbookingpage2"),
    path('payment/', views.payment, name="payment"),
    path('paymentcomp/', views.paymentcomp, name="paymentcomp"),
    path('transactions/', views.transactionsdef, name="transactionsdef"),
    path('viewtransactions/', views.viewtransactions, name="viewtransactions"),
    path('booksr/', views.booksr, name="booksr"),
    path('booksrd/', views.booksrd, name="booksrd"),
    path('booksrm/', views.booksrm, name="booksrm"),
    path('paymentcomp2/', views.paymentcomp2, name="paymentcomp2"),
    path('missing/', views.missing, name="missing"),
    
    
    

    
]
