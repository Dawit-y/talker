from django.urls import path
from . import views
urlpatterns = [
   
    

    path('', views.index, name="home"),
    path('login/', views.login_form, name="login"),
    path('register/', views.register, name="register"),
    path('logout/', views.logout_form, name="logout"),
]










