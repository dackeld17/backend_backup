from rest_framework import generics
from django.contrib.auth.models import User
from .models import Timeline
from .serializers import TimelineSerializer
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage  # default_storage 추가
from django.core.files.base import ContentFile
import os

class UserTimelineView(generics.ListAPIView):
    serializer_class = TimelineSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        username = self.kwargs.get('username')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound(detail="User not found.")

        return Timeline.objects.filter(user=user)

@method_decorator(csrf_exempt, name='dispatch')
class ImageUploadView(View):
    def get(self, request, *args, **kwargs):
        # GET 요청에 대한 응답
        return JsonResponse({"message": "This endpoint only supports POST for image upload."})

    def post(self, request, *args, **kwargs):
        # 'file'이라는 이름으로 전송된 파일 가져오기
        uploaded_file = request.FILES.get("file")
        if not uploaded_file:
            return JsonResponse({"message": "No file uploaded"}, status=400)

        # 파일 저장 경로 설정
        save_path = os.path.join("uploads", uploaded_file.name)
        path = default_storage.save(save_path, ContentFile(uploaded_file.read()))

        # 파일 저장 위치 확인
        return JsonResponse({"message": "Image uploaded successfully", "file_path": path})
