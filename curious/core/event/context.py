# This file is part of curious.
#
# curious is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# curious is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with curious.  If not, see <http://www.gnu.org/licenses/>.

"""
Represents the event context.
"""
import contextvars
import typing

from curious.core import client as md_client
from curious.core.gateway import GatewayHandler
from curious.internal.proxy import ProxyVar

_global_context = contextvars.ContextVar("event_context")

#: The event context global to use.
event_context = ProxyVar(_global_context)


class EventContext(object):
    """
    Represents a special context that are passed to events.
    """

    def __init__(self, cl: 'md_client.Client', shard_id: int,
                 event_name: str):
        """
        :param cl: The :class:`.Client` instance for this event context.
        :param shard_id: The shard ID this event is for.
        :param event_name: The event name for this event.
        """
        #: The :class:`.Client` instance that this event was fired under.
        self.bot = cl

        #: The shard this event was received on.
        self.shard_id = shard_id  # type: int
        #: The shard for this bot.
        self.shard_count = cl.shard_count  # type: int

        #: The event name for this event.
        self.event_name = event_name  # type: str

    @property
    def handlers(self) -> typing.List[typing.Callable[['EventContext'], None]]:
        """
        :return: A list of handlers registered for this event.
        """
        return self.bot.events.getall(self.event_name, [])

    async def change_status(self, *args, **kwargs) -> None:
        """
        Changes the current status for this shard.

        This takes the same arguments as :class:`.Client.change_status`, but ignoring the shard ID.
        """
        kwargs["shard_id"] = self.shard_id
        return await self.bot.change_status(*args, **kwargs)

    @property
    def gateway(self) -> GatewayHandler:
        """
        :return: The :class:`.Gateway` that produced this event.
        """
        return self.bot.gateways[self.shard_id]
