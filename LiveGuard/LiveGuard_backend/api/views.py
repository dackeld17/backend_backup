from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ImageUploadSerializer
import os

class ImageUploadView(APIView):
    def post(self, request):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            image_file = serializer.validated_data['image']
            image_path = os.path.join('/path/to/save', image_file.name)
            
            # 이미지 저장
            with open(image_path, 'wb') as f:
                for chunk in image_file.chunks():
                    f.write(chunk)
                    
            return Response({'message': 'Image uploaded successfully'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

