from rest_framework.serializers import ModelSerializer

from .models import Photo


class PhotoSerilizer(ModelSerializer):

    class Meta:
        model = Photo
        fields = (
            "pk",
            "file",
            "description",
        )
