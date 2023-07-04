import hashlib
import os

from django.conf import settings
from django.core.files.storage import default_storage
from django.http import FileResponse
from django.urls import reverse
from PIL import Image
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from .serializer import ResizePictureSerializer
from .helpers import resize_image

class ImageView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, image_name, **kwargs):
        image_path = os.path.join(settings.MEDIA_ROOT, image_name)
        if os.path.exists(image_path):
            return FileResponse(open(image_path, 'rb'), content_type='image/png')
        else:
            return Response({'error_message': 'Image not found'}, status=HTTP_400_BAD_REQUEST)


class ResizePictureView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResizePictureSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data.get('file')
        width = serializer.validated_data.get('width')
        height = serializer.validated_data.get('height', 0)

        with file.open(mode='rb') as image_file:
            image_url = resize_image(file.name, image_file, width, height)

        return Response({'url': image_url})
