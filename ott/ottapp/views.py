from django.shortcuts import render
from django.http import HttpResponse    
from django.views.decorators.cache import cache_control
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect
from .forms import AddMovieForm
from .models import Movie

from ottapp.driveapi.Google import Create_Service
from googleapiclient.http import MediaFileUpload
import mimetypes
import os
from ott import settings 
import uuid as uuid
import io
from googleapiclient.http import MediaIoBaseDownload


CLIENT_SECRET_FILE = 'ottapp/driveapi/client_secret_541522205044-1tutfoqle8ql6god85vfp7fbdvdiov6h.apps.googleusercontent.com.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = Create_Service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,SCOPES)



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


def upload(file1,name):
    with open('assets/tmp/'+file1.name, 'wb+') as destination:  
        for chunk in file1.chunks():  
            destination.write(chunk)  
            
            
    location = os.path.join(str(settings.BASE_DIR), 'assets')
    location = os.path.join(location, 'tmp')
    location = location + "\\"+file1.name
            
    folder_id = ['1v4Ap2MVlE7UcBp5EhEiXnEBmfUABNW9Y','1bnKl1dyOqsSiFf3HBdrVkzMvpvvbG_e1','1Wdm3y0DW7jKI0SATmFL_K6fx2mSvNx8a']
    
    if name == 'poster':
        file_metadata = {
            'name': file1.name,
            'parents' : [folder_id[0]]
        }
    elif name == 'trailer':
        file_metadata = {
            'name': file1.name,
            'parents' : [folder_id[1]]
        }
    else:
        file_metadata = {
            'name': file1.name,
            'parents' : [folder_id[2]]
        }
    media = MediaFileUpload(location, mimetype=mimetypes.guess_type(file1.name)[0])
    file = service.files().create(body=file_metadata,
                                    media_body=media,
                                    fields='id').execute()
            
    id = file.get('id')
    return id
    
    


def addmovie(request):
    print("in addmovie")
    if request.method == 'POST':
        form = AddMovieForm(request.POST,request.FILES)
        print("in apost")
        if form.is_valid():
            print("in valid")
            movie_name = form.cleaned_data['movie_name']
            
            p = request.FILES['poster']
            poster = request.FILES['poster'].name
            
            genre = form.cleaned_data['genre']
            release_date = form.cleaned_data['release_date']
            ratting = form.cleaned_data['ratting']
            running_time = form.cleaned_data['running_time']
            description = form.cleaned_data['description']
            
            v = request.FILES['video']
            video = request.FILES['video'].name
            
            t = request.FILES['trailer']
            trailer = request.FILES['trailer'].name
            
            
            id_poster = upload(p,"poster")
            id_trailer = upload(t,"trailer")
            id_video = upload(v,"video")
            
            m = Movie(movie_name=movie_name ,poster=id_poster,genre=genre,release_date=release_date,
                     ratting=ratting,running_time=running_time,description=description,video=id_video,trailer=id_trailer)
            
            m.save()
            
            location = os.path.join(str(settings.BASE_DIR), 'assets')
            location = os.path.join(location, 'tmp')
            location1 = location + "\\"+poster
            location2 = location + "\\"+trailer
            location3 = location + "\\"+video
            
            try:
                os.remove(location1)
                os.remove(location2)
                os.remove(location3)
            except:
                pass
            print(movie_name,poster,genre,release_date,ratting,running_time,description,video,trailer)
            
    form = AddMovieForm()
    return render(request,'addmovieform.html',{'form':form})