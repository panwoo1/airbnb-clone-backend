import typing

import strawberry

from . import queries, types


@strawberry.type
class Query:
    all_rooms = typing.List[types.RoomType] = strawberry.field(
        resolver=queries.get_all_rooms,
    )
