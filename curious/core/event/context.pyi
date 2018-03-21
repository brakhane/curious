"""
Represents the event context.
"""
import typing
from contextvars import ContextVar

from curious import Client, GatewayHandler

_global_context: ContextVar
#: The event context global to use.
event_context: EventContext


class EventContext(object):
    bot: Client
    shard_id: int
    shard_count: int
    event_name: str

    def __init__(self, cl: Client, shard_id: int, event_name: str): ...
    @property
    def handlers(self) -> typing.List[typing.Callable[['EventContext'], None]]: ...
    async def change_status(self, *args, **kwargs) -> None: ...
    def gateway(self) -> GatewayHandler: ...