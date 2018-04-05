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
Event management utilities.

.. currentmodule:: curious.core.event

.. autosummary::
    :toctree:

    manager
    decorator
    context
"""
import inspect
import typing

from curious.core.event.context import EventContext, event_context
from curious.core.event.decorator import event
from curious.core.event.manager import EventManager, ListenerExit

__all__ = [
    "EventContext", "event_context",
    "event",
    "EventManager"
]


def scan_events(obb) -> typing.Generator[None, typing.Tuple[str, typing.Any], None]:
    """
    Scans an object for any items marked as an event and yields them.
    """

    def _pred(f):
        is_event = getattr(f, "is_event", False)
        if not is_event:
            return False

        if not f.scan:
            return False

        return True

    for _, item in inspect.getmembers(obb, predicate=_pred):
        yield (_, item)