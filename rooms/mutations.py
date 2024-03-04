import typing
from enum import Enum

import strawberry
from django.db import transaction
from strawberry import ID
from strawberry.types import Info

from categories.models import Category

from .models import Amenity, Room


@strawberry.enum
class RoomKindChoices(Enum):
    ENTIRE_PLACE = "entire_place"
    PRIVATE_ROOM = "private_room"
    SHARED_ROOM = "shared_room"


@strawberry.input
class RoomInput:
    category_id: ID
    amenities: typing.List[ID]
    name: str
    country: str
    city: str
    price: int
    rooms: int
    toilets: int
    description: str
    address: str
    pet_friendly: bool
    kind: RoomKindChoices


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_room(
        info: Info,
        room_input: RoomInput,
    ) -> Room:
        try:
            category = Category.objects.get(pk=room_input.category_id)
        except Category.DoesNotExist:
            raise ValueError("Category is not found")

        if category.kind != Category.CategoryKindChoices.ROOMS:
            raise ValueError("Category must be a 'ROOMS' category")

        if len(room_input.amenities) > Amenity.objects.count():
            raise ValueError("Invalid amenities provided")

        try:
            with transaction.atomic():
                room = Room.objects.create(
                    name=room_input.name,
                    country=room_input.country,
                    city=room_input.city,
                    price=room_input.price,
                    rooms=room_input.rooms,
                    toilets=room_input.toilets,
                    description=room_input.description,
                    address=room_input.address,
                    pet_friendly=room_input.pet_friendly,
                    kind=room_input.kind,
                    owner=info.context.request.user,
                    category=category,
                )

                for amenity_id in room_input.amenities:
                    try:
                        amenity = Amenity.objects.get(pk=amenity_id)
                    except Amenity.DoesNotExist:
                        raise ValueError("Amenity is not found")
                    room.amenities.add(amenity)

                room.save()

                return room
        except Exception as e:
            raise ValueError(f"Error creating room: {e}")
