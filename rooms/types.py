import typing

import strawberry
from django.conf import settings
from strawberry import auto
from strawberry.types import Info

from reviews.types import ReviewType
from users.types import UserType
from wishlists.models import Wishlist

from . import models


@strawberry.django.type(models.Room)
class RoomType:
    id: auto
    name: auto
    kind: auto
    owner: "UserType"
    reviews: typing.List["ReviewType"]

    @strawberry.field
    def reviews(self, page: typing.Optional[int]) -> typing.List["ReviewType"]:
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        return self.reviews.all()[start:end]

    @strawberry.field
    def rating(self) -> str:
        return self.rating()

    @strawberry.field
    def is_owner(self, info: Info) -> bool:
        return self.owner == info.context.request.user

    @strawberry.field
    def is_liked(self, info: Info) -> bool:
        return Wishlist.objects.filter(
            user=info.context.request.user,
            room__pk=self.pk,
        ).exists()
