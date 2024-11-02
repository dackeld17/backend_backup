from django.urls import path
from .views import UserTimelineView
from .views import ImageUploadView

urlpatterns = [
    path('timeline/<str:username>/', UserTimelineView.as_view(), name='user-timeline'),
     path('upload_image/', ImageUploadView.as_view(), name='upload_image'),
]
