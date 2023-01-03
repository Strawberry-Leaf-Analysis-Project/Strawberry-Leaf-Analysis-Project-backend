from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('board',views.board_home,name="board_home"),
    path('board_write',views.board_write,name="board_write"),
    path('board_newWrite',views.board_newWrite,name="board_newWrite"),
    path('board_detail/<int:key>',views.board_detail,name="board_detail")
]
