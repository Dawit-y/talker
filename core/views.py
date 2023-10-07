from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from .forms import UserRegistrationForm
from .models import *


@login_required
def index(request):
    user = request.user
    profile = Profile.objects.get(user = user)
    posts = Post.objects.all().prefetch_related('comments')
    return render(request, 'core/index.html' , {'profile' : profile, 'posts' : posts})


def login_form(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')

        try:
            user = User.objects.get(username = username)   
        except:
            messages.error(request, 'User doesnt exist')
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else :
            messages.error(request, 'something went wrong')

    return render(request, 'core/login.html', {})

def register(request):
    form = UserRegistrationForm()
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, form.error_messages)
            print(form.error_messages)
            form = UserRegistrationForm()
    return render(request, 'core/register.html', {'form' : form})

def logout_form(request):
    logout(request)
    return redirect('login')

def create_like(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        profile_id = request.POST.get('profile_id')

        post = Post.objects.get(pk = post_id)
        profile = Profile.objects.get(pk = profile_id)
        
        try:
            like = Like.objects.get(likedPost = post)
            if like.likedBy.contains(profile):
                like.likedBy.remove(profile)
            else:
                like.likedBy.add(profile)
        except:
            like = Like.objects.create(likedPost = post)
            like.likedBy.add(profile)
        return JsonResponse({'status': 'success', 'message': 'Like created!'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

def comment(request):
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        profile_id = request.POST.get("user_id")
        content = request.POST.get("comment")
        post = Post.objects.get(pk = post_id)
        profile = Profile.objects.get(pk = profile_id)

        comment = Comment.objects.create(author=profile, post= post, content=content)
        return redirect(request.META.get('HTTP_REFERER', '/'))
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})