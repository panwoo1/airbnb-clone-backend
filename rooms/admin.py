from django.contrib import admin

from .models import Amenity, Room

# Register your models here.


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "price",
        "kind",
        "owner",
        "total_amenities",
    )

    list_filter = (
        "country",
        "city",
        "price",
        "rooms",
        "toilets",
        "pet_friendly",
        "kind",
        "amenities",
    )


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "description",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
