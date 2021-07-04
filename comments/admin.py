from comments.models import Comments
from django.contrib import admin

# Register your models here.

@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    list_filter = ['message', "author", "doctor"]