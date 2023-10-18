from django.urls import path
from . import views
urlpatterns = [
    path('', views.friends, name="friends"),
    path('friend_request/', views.friend_request, name="friend_request"),
    path('sent_request/', views.sent_request, name="sent_request"),
    path('find_friends/', views.find_friends, name="find_friends"),

    path('request/<int:id>/', views.send_friend_request, name="friend_request"),
    path('accept/<int:id>/', views.accept_request, name="accept_request"),
    path('reject/<int:id>/', views.reject_request, name="reject_request"),
    path('cancel/<int:id>/', views.cancel_request, name="cancel_request"),

    path('notification/', views.notification, name="notification"),
]