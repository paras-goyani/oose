from django.shortcuts import render
from django.http import HttpResponse    
from django.views.decorators.cache import cache_control
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect
from .forms import AddMovieForm
from .models import Movie,user_plan,subscription_plan
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from ottapp.driveapi.Google import Create_Service
from googleapiclient.http import MediaFileUpload
import mimetypes
import os
from ott import settings 
import io
from googleapiclient.http import MediaIoBaseDownload


CLIENT_SECRET_FILE = 'ottapp/driveapi/client_secret_541522205044-1tutfoqle8ql6god85vfp7fbdvdiov6h.apps.googleusercontent.com.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = Create_Service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,SCOPES)


@login_required(login_url='signin')
def home(request):
    movies = Movie.objects.all()
    print("======================== ",len(movies))
    for m in movies:
        print(m.description)
    return render(request,'home.html',{'movies' : movies})

def login(request):
    return HttpResponse("Hello")


def signin(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = auth.authenticate(username=username, password=password)
    print(user)
    if request.method == 'POST':
        if user is not None:
            
            try:
                del request.session['user_plan']
                
            except:
                pass
            
            auth.login(request, user)
            
            user_plan1 = user_plan.objects.get(username=username)
            request.session['user_plan'] = user_plan1.plan_name
            
            if username == "admin" and password == "admin":
                request.session['admin'] = "admin"
            
            print(request.session['user_plan'])
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
                
                user_subscription = user_plan(username=username,plan_name='-1')
                user_subscription.save()
                
                request.session["user_plan"] = "-1"
                return render(request, 'signin.html')
        else:
            exist='password does not match'
            return render(request, 'signup.html', {'exist': exist})

    return render(request, 'signup.html')

@login_required(login_url='signin')
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
    
    

@login_required(login_url='signin')
def addmovie(request):
    print("in addmovie")
    
    if 'admin' in request.session:
        
    
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
                plan = form.cleaned_data['plan']
                
                v = request.FILES['video']
                video = request.FILES['video'].name
                
                t = request.FILES['trailer']
                trailer = request.FILES['trailer'].name
                
                
                id_poster = upload(p,"poster")
                id_trailer = upload(t,"trailer")
                id_video = upload(v,"video")
                
                m = Movie(movie_name=movie_name ,poster=id_poster,genre=genre,release_date=release_date,
                        ratting=ratting,running_time=running_time,description=description,video=id_video,trailer=id_trailer,plan=plan)
                
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
                return render(request,'/home')
    else:
        return render(request,'admin_authentication.html')
            
    form = AddMovieForm()
    return render(request,'addmovieform.html',{'form':form})



@login_required(login_url='signin')
def detail(request,id):
    
    id =int(id)
    usr = request.user.username;
    
    movie = Movie.objects.get(id=id)
    
    is_plan_available =False
    user_plan = request.session['user_plan']
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(user_plan)
    print(movie.plan)
    
    print(request.session['user_plan'])
    if(user_plan == '-1'):
        is_plan_available = False
    elif (user_plan == 'basic' or user_plan == 'premium' or user_plan == "cinematic") and movie.plan == 'basic':
        is_plan_available = True
    elif (user_plan == 'premium' or user_plan == "cinematic") and movie.plan == 'premium':
        is_plan_available = True
    elif (user_plan == "cinematic") and movie.plan == 'premium':
        is_plan_available = True
    elif (user_plan == "cinematic") and movie.plan == 'cinematic':
        is_plan_available = True
    else :
        is_plan_available = False
        
        
    print(id)
    
    return render(request,'details.html',{'movie':movie , 'is_plan_available':is_plan_available})

@login_required(login_url='signin')
def download(request,id):
    
    file_id = id
    username = request.user.username

    
    request = service.files().get_media(fileId = file_id)
        
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fd =fh,request = request)
    done = False
        
    while not done:
        status , done = downloader.next_chunk()
        print('Progress ',format(status.progress() *100))
            
    fh.seek(0)
    
    with open(os.path.join("./ottapp/Downloads/","movie.mp4"),'wb') as f:
        f.write(fh.read())
        f.close()
    
    return HttpResponse("download complete")

@login_required(login_url='signin')
def pricing(request):
    
    all_plan = subscription_plan.objects.all()
    
    
    return render(request , 'pricing.html',{'all_plan':all_plan})

@login_required(login_url='signin')
def handle_page_not_found_404(request):
    
    page_title='Page Not Found'
    return render(request,'404.html')

@login_required(login_url='signin')
def select_plan(request,plan_name):
    username1 = request.user.username
    
    print(username1)
    t = user_plan.objects.get(username=username1)
    t.plan_name = plan_name
    t.save()
    request.session['user_plan'] = plan_name
    
    return render(request,'plan_purchased.html')

@login_required(login_url='signin')
def logout(request):
    logout1 = 'you are successfully logout'
    auth.logout(request)
    messages.info(request,logout1)
    return render(request, 'signin.html', {'logout': logout1})
    