import strawberry
from strawberry import auto

from users.types import UserType

from . import models


@strawberry.django.type(models.Room)
class RoomType:
    id: auto
    name: auto
    kind: auto
    owner: "UserType"
