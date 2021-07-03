from django.contrib import admin
from doctorsUser.models import DoctorUser


@admin.register(DoctorUser)
class UsersAdminPanel(admin.ModelAdmin):
    list_display = ['fullname', 'is_active']
    list_filter = ['fullname', 'email', 'is_active']