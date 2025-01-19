# 각 앱의 api 라우팅
from django.urls import path, include
from .views import ImageUploadView
from django.contrib import admin
from django.urls import path
from api import views  # api 앱의 views를 가져옴

urlpatterns = [
    path('api/', include('density.urls')),
    path('api/upload_image/', ImageUploadView.as_view(), name='upload_image'),
   
    # 다른 앱의 URL도 필요 시 포함
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # 홈 화면
    path('live_feed/', views.live_feed, name='live_feed'),  # CCTV 보기 페이지

]
