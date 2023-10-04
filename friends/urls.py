from django.urls import path
from . import views
urlpatterns = [
   
    path('request/<int:id>/', views.send_friend_request, name="friend_request"),
    path('notification/', views.notification, name="notification")
]