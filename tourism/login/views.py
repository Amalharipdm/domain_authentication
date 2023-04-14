from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth


# Create your views here.
def homePage(request):
    if 'username' in request.session:
        return render(request, "home.html")
    return redirect(login)



def register(request):
    if 'username' in request.session:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username taken')
                print('Username taken')

                return redirect('register')
            else:
                user = User.objects.create_user(username=username,password=password1)
                user.save()
                print('user created')
                messages.info(request, 'User created')
            return redirect('login')
        else:
            messages.info(request, 'password not matching')
            print('password not matching..')
            return redirect('register')
    else:
        return render(request, 'register.html')
    

def login(request):
    if 'username' in request.session:
        return redirect('/')
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            request.session['username']=username   #sessions
            return redirect("/")
        else:
            messages.info(request, 'invalid credentials')
            return redirect('login')
    else:
        return render(request,'login.html')
    
def logout(request):
    if 'username' in request.session:
        request.session.flush()
    return redirect('register')