from django.urls import path
from django.conf.urls import include

from . import views

urlpatterns = [
    path('members/new', views.member_register, name="member_register"),
    path('members/member_idcheck',views.member_idcheck,name="member_idcheck"),
    path('members/member_insert',views.member_insert,name="member_insert"),
    path('login', views.login, name="login"),
    path('member_login', views.member_login, name="member_login"),
    path('member_logout', views.member_logout, name="member_logout"),
    path('member_statchange', views.member_statchange, name="member_statchange"),
    path('member_changeName', views.member_changeName, name="member_changeName"),
    path('member_changePassword', views.member_changePassword, name="member_changePassword"),
]
