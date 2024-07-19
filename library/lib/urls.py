from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('login/',views.loginn,name='login'),
    path("signup/",views.signup,name="signup"),
    path('logout/',views.logoutt,name="logout"),
    path('profile/',views.profile,name="profile"),
    path('borrow/',views.borrow,name = "borrow"),
    path('sucess',views.sucess,name = "sucess"),
    path('return_book',views.return_book,name="return_book"),
    
     
]