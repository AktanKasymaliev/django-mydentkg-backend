from customUser.models import User
from django.contrib import admin

@admin.register(User)
class UsersAdminPanel(admin.ModelAdmin):
    list_display = ['username', 'is_active']
    list_filter = ['username', 'email', 'is_active']