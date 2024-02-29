from rest_framework import serializers

from categories.serializers import CategorySerializer
from medias.serializers import PhotoSerializer, VideoSerializer
from rooms.serializers import TinyUserSerializer
from wishlists.models import Wishlist

from . import models


class ExperienceListSerializer(serializers.ModelSerializer):

    is_owner = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)
    video = VideoSerializer(read_only=True)

    class Meta:
        model = models.Experience
        fields = (
            "pk",
            "name",
            "photos",
            "video",
            "country",
            "city",
            "price",
            "is_owner",
            # "is_liked",
        )

    def get_is_owner(self, experience):
        request = self.context["request"]
        return experience.host == request.user


class ExperienceDetailSerializer(serializers.ModelSerializer):

    host = TinyUserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    is_owner = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)
    video = VideoSerializer(read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = models.Experience
        fields = "__all__"

    def get_is_owner(self, experience):
        request = self.context["request"]
        return experience.host == request.user

    def get_is_liked(self, experience):
        request = self.context["request"]
        return Wishlist.objects.filter(
            user=request.user, experiences__pk=experience.pk
        ).exists()


class PerkSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Perk
        fields = "__all__"
