from django.urls import path
from django.urls import re_path
from django.views.generic import TemplateView
from .views import handle_page_not_found_404


from . import views


urlpatterns = [
    
    path('',views.signin,name="signin"),
    path('signin',views.signin,name="signin"),
    path('signup',views.signup,name="signup"),
    path('home',views.home,name="home"),
    path('addmovie',views.addmovie,name="addmovie"),
    path('detail/<int:id>',views.detail,name="detail"),
    path('download/<str:id>',views.download,name="download"),
    re_path(r'^pricing', views.pricing, name='pricing'),
    path('select_plan/<str:plan_name>', views.select_plan, name='pricing'),
    path('logout',views.logout,name='logout')
    #re_path(r'^/*',views.handle_page_not_found_404,name="404")
]
