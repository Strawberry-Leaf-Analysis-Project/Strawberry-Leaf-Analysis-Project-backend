from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)