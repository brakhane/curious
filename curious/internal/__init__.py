"""
This package contains various scary internals. Anything that is re-exported inside the package
init is considered a stable API, and anything not is an unstable, not-for-usage API.

.. currentmodule:: curious.internal

.. autosummary::
    :toctree:

    contextvars_inject
"""
from curious.internal.contextvars_inject import contextvars_inject

__all__ = [
    "contextvars_inject"
]
