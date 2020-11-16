"""biscuits URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from biscuitsrk import views
from django.views.static import serve
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('comingsoon/',views.coming_soon,name="coming_soon"),
    path('ended/',views.ended,name="ended"),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('login/', views.loginuser, name='loginuser'),
    path('signup/', views.signupuser, name='signupuser'),
    path('questions/', views.questions, name='questions'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('checkanswers/', views.checkanswers, name='checkanswers'),
    path('fullanswer/<int:id>', views.fullanswer, name='fullanswer'),
]
