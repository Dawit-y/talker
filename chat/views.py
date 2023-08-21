from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required()
def lobby(request):
    return render(request, 'chat/lobby.html', {})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')

        print(username, password)
    return render(request, 'chat/login.html', {})

# def one(request):
#     return render(request, 'chat/one.html', context={'one_text': "ASD"})

# def index(request):
#     return render(request, "chat/index.html")


# def room(request, room_name):
#     return render(request, "chat/room.html", {"room_name": room_name})

# def two(request):
#     return render(request, 'chat/two.html')