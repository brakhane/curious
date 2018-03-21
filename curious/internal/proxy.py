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
Represents a context var proxy.
"""
from contextvars import ContextVar

class ProxyVar(object):
    """
    Proxies attribute access to a context var.
    """
    def __init__(self, cvar: ContextVar):
        self.__dict__["_cvar"] = cvar

    def __getattr__(self, item):
        return getattr(self._cvar.get(), item)

    def __setattr__(self, key, value):
        return setattr(self._cvar.get(), key, value)

    # compat
    def __repr__(self):
        return repr(self._cvar.get())

    def __str__(self):
        return str(self._cvar.get())

    def unwrap_context(self):
        """
        Unwraps this context to get the data of the underlying object.
        """
        return self._cvar.get()