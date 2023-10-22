from django.urls import path
from . import views
urlpatterns = [
 
    path('', views.index, name="home"),
    path('login/', views.login_form, name="login"),
    path('register/', views.register, name="register"),
    path('logout/', views.logout_form, name="logout"),
    path('post/', views.create_post, name = "create_post"),
    path('like/', views.create_like, name='create_like'),
    path('comment/', views.comment, name="comment"),
    path('test/', views.test, name="test")
]










