from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings

from rest_framework import routers
from board import views as board_views
from member import views as member_views
from models import views as models_views
from models.views import Train,Predict

urlpatterns = [
    path('train/',Train.as_view(),name="train"),
    path('predict/',Predict.as_view(),name="predict"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
