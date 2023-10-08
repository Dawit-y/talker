from django.urls import path
from . import views
urlpatterns = [
    path('', views.friends, name="friends"),
    path('friend_request/', views.friend_request, name="friend_request"),
    path('sent_request/', views.sent_request, name="sent_request"),
    path('request/<int:id>/', views.send_friend_request, name="friend_request"),
    path('notification/', views.notification, name="notification")
]