from django.contrib import admin
from .models import Board
from member.models import Member
# Register your models here.

admin.site.register(Board)
admin.site.register(Member)