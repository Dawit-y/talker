from django.urls import path
from . import views
urlpatterns = [
    path('', views.lobby, name="home"),
    path('login/', views.login, name="login")
   
    
]