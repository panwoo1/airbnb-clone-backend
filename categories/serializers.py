from rest_framework import serializers

from .models import Category


class CategorySerilizer(serializers.Serializer):

    pk = serializers.IntegerField(read_only=True)
    name = serializers.CharField(
        required=True,
        max_length=50,
    )
    kind = serializers.CharField()

    created_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.kind = validated_data.get("kind", instance.kind)
        instance.save()
        return instance
