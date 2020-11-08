from datetime import datetime, timezone,timedelta

from .models import QuestionsModel, Profile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
import re
# Create your views here.
def coming_soon(request):
	return render(request, 'biscuitsrk/comingson.html')
def check_coming_soon():
	now = datetime.utcnow()
	# now+=timedelta(hours = 5,minutes=30)
	# dt_string = "16/11/2020 12:30:00"
	dt = datetime(2020,11,17,23,59) # Year, Month, Date, Hours, Minutes, ## Seconds
	dt+=timedelta(hours = -5,minutes= -30)
	print(now,dt)
	if(now<dt):
		return True
	return False

@login_required
def questions(request):
    if(check_coming_soon()):
        return redirect('coming_soon')
    u = get_object_or_404(Profile,user=request.user)

    if request.method=='GET':
        if u.answered == True:
            # print("Path A")
            # if(u.result)
            question = get_object_or_404(QuestionsModel, level=u.currentlevel)
            return render(request, 'biscuitsrk/questionsBlank.html',{'question':question,'u':u})
        # print("Path B")
        question = get_object_or_404(QuestionsModel, level=u.currentlevel)
        return render(request, 'biscuitsrk/questions.html',{'question':question,'u':u})
    if request.POST :
        if len(request.POST['answer']) == 0:
            question = get_object_or_404(QuestionsModel, level=u.currentlevel)
            return render(request, 'biscuitsrk/questions.html',{'question':question, 'error':'Answer Box Cannot be empty'})
        else:
            u.mostrecentanswer = request.POST['answer']
            u.lastanswertime = timezone.now()
            u.checked = False
            u.answered = True
            u.save()
            return redirect('questions')
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
    if not re.search(".*#[0-9]{4}$",request.POST["discord"]):
        return render(request, 'biscuitsrk/signup.html', {'form':UserCreationForm(),'error':'The Discord username is not valid'})
    if request.POST['password1']==request.POST['password2']:
        try:
            user = User.objects.create_user(request.POST['username'],password=request.POST['password1'])
            user.save()
            u = get_object_or_404(Profile,user=user)
            print(u)
            u.institute = request.POST["institute"]
            u.discord = request.POST["discord"]
            u.answered = False
            print(u)
            u.save()
            login(request, user)
            return redirect('questions')
        except IntegrityError:
            return render(request, 'biscuitsrk/signup.html', {'form':UserCreationForm(),'error':'This Username has been already taken.'})
    else:
            return render(request, 'biscuitsrk/signup.html', {'form':UserCreationForm(),'error':'Both passwords do not match'})
def home(request):
	return render(request, 'biscuitsrk/home.html')
def leaderboard(request):
	if(check_coming_soon()):
		return redirect('coming_soon')
	"""
	Returns the leadboard, sorted first with level (desc) then time (asc)
	"""
	queryset = Profile.objects.order_by('-currentlevel','currentleveltime')
	context = {
		'queryset' : queryset,
	}
	return render(request, 'biscuitsrk/leaderboard.html', context)
@user_passes_test(lambda u: u.is_superuser)
def checkanswers(request):
    queryset = Profile.objects.order_by('-lastanswertime')
    return render(request, 'biscuitsrk/checkanswers.html',{'answers':queryset})
@user_passes_test(lambda u: u.is_superuser)
def fullanswer(request, id):
    u = get_object_or_404(Profile, pk=id)
    if request.method == 'GET':
        return render(request, 'biscuitsrk/fullanswer.html',{'u':u})
    else:
        if request.POST['check']=='correct':
            level= int(request.POST['level'])
            u.result = True
            u.checked = True
            u.response = ''
            u.currentlevel = level + 1
            u.currentleveltime = timezone.now()
            u.answered = False
            u.mostrecentanswer = ""
            u.save()
            return redirect('checkanswers')
        elif request.POST['check']=='incorrect':
            u.result = False
            u.checked = True
            u.answered = False
            u.response = request.POST['response']
            u.save()
            return redirect('checkanswers')
        elif request.POST['check']=='correcting':
            return redirect('checkanswers')
