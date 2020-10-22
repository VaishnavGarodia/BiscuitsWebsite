from django.contrib import admin
from .models import QuestionsModel, Profile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
admin.site.register(QuestionsModel)
admin.site.register(Profile)
