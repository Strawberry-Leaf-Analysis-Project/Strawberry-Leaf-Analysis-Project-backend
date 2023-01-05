from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.home,name="home"),
    path('board',views.board_home,name="board_home"),
    path('board_write',views.board_write,name="board_write"),
    path('board_newWrite',views.board_newWrite,name="board_newWrite"),
    path('board_detail/<int:key>/<int:flag>',views.board_detail,name="board_detail"),
    path('board_delete/<int:key>/<int:flag>',views.board_delete,name="board_delete"),
    path('personal_board',views.personalBoard_home,name="personalBoard_home"),
] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
