from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings

from rest_framework import routers
from board import views as board_views
from member import views as member_views
from disease import views as disease_views
from plants_detail import views as plants_detail_views
from plants_by_disease import views as plants_by_disease_views
from plants_group import views as plants_group_views
#from temp_image import views as temp_image_views
import models.urls

router = routers.DefaultRouter()
router.register(r'member', member_views.MemberListAPI)
router.register(r'board', board_views.BoardListAPI)
router.register(r'disease', disease_views.DiseaseListAPI)
router.register(r'plants_detail', plants_detail_views.PlantsDetailListAPI)
router.register(r'plants_by_disease', plants_by_disease_views.PlantsByDiseaseListAPI)
router.register(r'plants_group', plants_group_views.PlantsGroupListAPI)
#router.register(r'temp_image',temp_image_views.TempImageListAPI)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(router.urls)),
    path('models/',include(models.urls)),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)