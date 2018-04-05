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
Home of the default help command.

.. currentmodule:: curious.commands.help
"""
import inspect
from typing import List

from curious.commands.context import channel, command_context
from curious.commands.exc import CommandsError
from curious.commands.utils import get_full_name, get_usage


async def get_command_list(command, *, include_root: bool = True) -> List[str]:
    """
    Recursively produces a command list for the command, using subcommands.

    :param command: The command function to use.
    :param include_root: If the root command should be included in the list.
    :return: A list of command names.
    """
    ctx = command_context.get()
    try:
        if not (await ctx.can_run(command))[0]:
            return []
    except CommandsError:
        return []

    # XXX: Don't add command names if they're subcommands.
    if not command.cmd_subcommand and include_root:
        l = [command.cmd_name]
    else:
        l = []

    for subcommand in command.cmd_subcommands:
        # don't do hidden subcommands
        if getattr(subcommand, "cmd_hidden", False) is True:
            continue

        # only do subcommands that can be ran
        try:
            can_run, _ = await ctx.can_run(command)
        except CommandsError:
            can_run = False

        if not can_run:
            continue

        if include_root:
            l.append(get_full_name(subcommand))
        else:
            l.append(subcommand.cmd_name)
        l.extend(await get_command_list(subcommand))

    return l


async def help_for_all():
    """
    Gets the content of help for all.
    """
    # rows is a list of messages for a help row
    rows = []
    # row_num is the current number to put on a row
    # this isn't incremented if we skip a row
    row_num = 0
    ctx = command_context.get()

    for plugin in ctx.manager.plugins.values():
        commands = plugin._get_commands()
        command_names = []

        for command in commands:
            # check for hidden annotation
            if getattr(command, "cmd_hidden", False) is True:
                continue

            # don't add subcommands on their own
            # they are detected automatically by the command list loader
            if command.cmd_subcommand:
                continue

            names = await get_command_list(command)
            command_names.extend(names)

        if not command_names:
            continue

        row_num += 1
        # wrap the command names in backticks
        # and join it all up with some pipes
        names_joined = ' | '.join(f"`{c}`" for c in command_names)
        plugin_name = getattr(plugin, "plugin_name", plugin.__class__.__name__)
        rows.append(f"**{row_num}. {plugin_name}:** {names_joined}")

    # add any uncategorized commands
    if ctx.manager.commands:
        command_names = []

        for command in ctx.manager.commands.values():
            if command.cmd_subcommand:
                continue

            names = await get_command_list(command)
            command_names.extend(names)

        if command_names:
            row_num += 1
            names_joined = ' | '.join(f"`{c}`" for c in command_names)
            rows.append(f"**{row_num}. Uncategorized:** {names_joined}")

    if not rows:
        return "**You cannot run any commands.**"

    # add a preamble
    preamble = "**Commands:**\nUse `help <command>` for more information about a command.\n\n"

    rows_joined = '\n'.join(rows)
    return f"{preamble}{rows_joined}"


async def help_for_one(command):
    """
    Gets the content of help for one command.
    """
    ctx = command_context.get()
    # get the command from the manager
    cfunc = ctx.manager.get_command(command)
    if cfunc is None:
        return f"No such command: **`{command}`**"

    usage = get_usage(cfunc, invoked_as=command)

    subcommands = await get_command_list(cfunc, include_root=False)
    subcommands_fmtted = " | ".join(f"`{x}`" for x in subcommands)

    description = inspect.getdoc(cfunc)
    if description is None:
        description = "No description."

    if subcommands:
        return f"`{usage}`\n\n{description}\n\n**Subcommands:** {subcommands_fmtted}"
    else:
        return f"`{usage}`\n\n{description}"


async def help_command(*, command: str = None):
    """
    The default help command.
    """
    if command is None:
        # Let the ruling classes tremble at a Communistic revolution.
        # The proletarians have nothing to lose but their chains. They have a world to win.
        content = await help_for_all()
    else:
        # Evidence-based policy
        content = await help_for_one(command)

    await channel.messages.send(content)
