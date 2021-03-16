from django.shortcuts import render
from django.http import HttpResponse    
from django.views.decorators.cache import cache_control
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect

# Create your views here.

def home(request):
    return render(request,'index.html',{'name' : "paras"})

def login(request):
    return HttpResponse("Hello")


def signin(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = auth.authenticate(username=username, password=password)
    print(user)
    if request.method == 'POST':
        if user is not None:
            auth.login(request, user)
            return redirect("/home")
        else:
            # messages.info(request, 'invalid credentials')
            invalid="Username or Password is invalid"
            return render(request, 'signin.html',{'invalid':invalid})
    else:
        return render(request, 'signin.html')
    
    

def signup(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        re_password = request.POST.get("re_password")
        
        
        if password == re_password:
            if User.objects.filter(username=username).exists():
                exist="user is already exists"
                return render(request,'signup.html',{'exist':exist})
            else:
                user = User.objects.create_user(username=username, password=password,email=email)
                user.save()
                return render(request, 'signin.html')
        else:
            exist='password does not match'
            return render(request, 'signup.html', {'exist': exist})

    return render(request, 'signup.html')