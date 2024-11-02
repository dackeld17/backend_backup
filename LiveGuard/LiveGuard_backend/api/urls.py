# 각 앱의 api 라우팅
from django.urls import path, include
from .views import ImageUploadView

urlpatterns = [
    path('api/', include('density.urls')),
    path('api/upload_image/', ImageUploadView.as_view(), name='upload_image'),
    # 다른 앱의 URL도 필요 시 포함
]
