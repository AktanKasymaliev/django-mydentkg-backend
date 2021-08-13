from django.contrib import admin
from doctorsUser.models import DoctorUser, Reception, Reserve

class ReceptionAdmin(admin.StackedInline):
    model = Reception
    fk_name = "client_user"

@admin.register(DoctorUser)
class UsersAdminPanel(admin.ModelAdmin):
    list_display = ['fullname', 'is_active']
    list_filter = ['fullname', 'email', 'is_active']
    inlines = [ReceptionAdmin, ]

admin.site.register(Reception)
admin.site.register(Reserve)