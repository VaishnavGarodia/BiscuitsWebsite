from .models import QuestionsModel, Profile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
# Create your views here.
@login_required
def questions(request):
    u = get_object_or_404(Profile,user=request.user)
    if request.method=='GET':
        question = get_object_or_404(QuestionsModel, level=u.currentlevel)
        return render(request, 'biscuitsrk/questions.html',{'question':question})
    if request.POST :
        if len(request.POST['answer']) == 0:
            question = get_object_or_404(QuestionsModel, level=u.currentlevel)
            return render(request, 'biscuitsrk/questions.html',{'question':question, 'error':'Answer Box Cannot be empty'})
        else:
            u.mostrecentanswer = request.POST['answer']
            u.lastanswertime = timezone.now()
            u.checked = False
            u.save()
            return redirect('waiting')
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
    queryset = Profile.objects.order_by('lastanswertime')
    return render(request, 'biscuitsrk/checkanswers.html',{'queryset':queryset})
def waiting(request):
    u = get_object_or_404(Profile,user=request.user)
    if u.checked == False:
        return render(request, 'biscuitsrk/waiting.html')
    else:
        if u.result == False:
            response = u.response
            return render(request, 'biscuitsrk/incorrect.html', {'response':response})
        else:
            level=u.currentlevel
            u.currentlevel = level + 1
            u.checked = False
            u.result = False
            u.response = ''
            u.currentleveltime = timezone.now()
            u.save()
            return redirect('questions')
