from rest_framework import serializers

from .models import User


class TinyUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "name",
            "avatar",
            "username",
        )


class PrivateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = (
            "password",
            "is_superuser",
            "id",
            "is_staff",
            "is_active",
            "first_name",
            "last_name",
            "groups",
            "user_permissions",
        )


class PublicSerializer(serializers.ModelSerializer):

    rooms_count = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "avatar",
            "name",
            "gender",
            "rooms_count",
            "reviews_count",
        )

    def get_rooms_count(self, user):
        return user.rooms.count()

    def get_reviews_count(self, user):
        return user.reviews.count()
