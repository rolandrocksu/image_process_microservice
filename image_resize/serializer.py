from rest_framework import serializers


class ResizePictureSerializer(serializers.Serializer):
    file = serializers.ImageField()
    width = serializers.IntegerField()
    height = serializers.IntegerField(required=False)
