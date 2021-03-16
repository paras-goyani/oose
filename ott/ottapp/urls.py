from django.urls import path
from django.urls import re_path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    
    path('',views.signin,name="signin"),
    path('signin',views.signin,name="signin"),
    path('signup',views.signup,name="signup"),
    path('home',views.home,name="home")
   
]