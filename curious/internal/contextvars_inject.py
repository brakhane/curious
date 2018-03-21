"""
Injects Python 3.7 contextvars support into 3.6 (by editing sys.modules).
"""
import sys

def contextvars_inject():
    # non-567 impl, maybe?
    # if so, don't touch
    if 'contextvars' in sys.modules:
        return

    # we might have it already, so let's see
    try:
        import contextvars
    except ModuleNotFoundError:
        pass
    else:
        return

    # we don't, so let's just redirect the pep567 package to contextvars
    import pep567
    sys.modules['contextvars'] = pep567