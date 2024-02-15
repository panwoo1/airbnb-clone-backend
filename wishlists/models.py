from django.db import models

from common.models import CommonModel

# Create your models here.


class Wishlist(CommonModel):
    """Wishlist Model Definition"""

    name = models.CharField(max_length=150)
    rooms = models.ManyToManyField(
        "rooms.Room",
        releated_name="wishlists",
    )
    experiences = models.ManyToManyField(
        "experiences.Experience",
        releated_name="wishlists",
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        releated_name="wishlists",
    )

    def __str__(self) -> str:
        return self.name
