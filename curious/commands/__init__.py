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
Commands helpers.

.. currentmodule:: curious.commands

.. autosummary::
    :toctree: commands

    manager
    context
    decorators
    plugin
    utils
    ratelimit
    help

    exc
    converters
"""
from curious.commands.context import (Context, author, channel, command_context, guild, message)
from curious.commands.decorators import command, condition, ratelimit
from curious.commands.manager import CommandsManager
from curious.commands.plugin import Plugin
from curious.commands.ratelimit import BucketNamer
