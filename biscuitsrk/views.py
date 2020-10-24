from django.shortcuts import render
from .models import QuestionsModel, Profile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def questions(request):
    u = get_object_or_404(Profile,user=request.user)
    question = get_object_or_404(QuestionsModel, level=u.currentlevel)
    return render(request, 'biscuitsrk/questions.html',{'question':question})
@login_required
def logoutuser(request):
    if request.method=='POST':
        logout(request)
        return redirect('home')
        
def loginuser(request):
    if request.method=='GET':
        return render(request, 'biscuitsrk/login.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request,username = request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request, 'biscuitsrk/login.html', {'form':AuthenticationForm(), 'error':"username and password did not match."})
        else:
            login(request, user)
            return redirect('questions')
def signupuser(request):
    if request.method=='GET':
        return render(request, 'biscuitsrk/signup.html', {'form':UserCreationForm()})
    if request.POST['password1']==request.POST['password2']:
        try:
            user = User.objects.create_user(request.POST['username'],password=request.POST['password1'])
            user.save()
            login(request, user)
            return redirect('questions')
        except IntegrityError:
            return render(request, 'biscuitsrk/signup.html', {'form':UserCreationForm(),'error':'This Username has been already taken.'})
    else:
            return render(request, 'biscuitsrk/signup.html', {'form':UserCreationForm(),'error':'Both passwords do not match'})
def home(request):
    return render(request, 'biscuitsrk/home.html')
def leaderboard(request):
    pass
