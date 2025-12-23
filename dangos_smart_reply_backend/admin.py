from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'image', 'is_superuser', 'is_staff', 'is_active', 'date_joined')

admin.site.register(CustomUser, CustomUserAdmin)