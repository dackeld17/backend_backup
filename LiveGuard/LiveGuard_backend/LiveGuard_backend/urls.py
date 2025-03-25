"""
URL configuration for LiveGuard_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.conf.urls.static import static
from django.conf import settings
from api import views
import os


def display_image(request, image_name):
    # 미디어 디렉토리에서 이미지 파일 찾기
    image_path = os.path.join(settings.BASE_DIR, "websocket/frame", image_name)
    if os.path.exists(image_path):
        with open(image_path, 'rb') as f:
            return HttpResponse(f.read(), content_type="image/jpeg")
    return HttpResponse("Image not found", status=404)

def home(request):
    return HttpResponse("!Welcome TO LiveGuard!")

urlpatterns = [
   # path('admin/', admin.site.urls),
    path('api/', include('density.urls')),# density 앱의 URLs 포함
    path('api/', include('api.urls')),
    path('',views.home, name='home'),
    path('live_feed/', views.live_feed, name='live_feed'),
    path('image/<str:image_name>/', display_image, name='display_image'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

