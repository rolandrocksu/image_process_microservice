from django.urls import path
from .views import ResizePictureView, ImageView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', ResizePictureView.as_view(), name='resize_picture'),
    path('image/<str:image_name>/', ImageView.as_view(), name='image')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
