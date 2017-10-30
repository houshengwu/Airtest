# _*_ coding:UTF-8 _*_
import atexit
import sys
from functools import wraps
from .compat import str_class


def split_cmd(cmds):
    """Split cmd to list, for subprocess."""
    if isinstance(cmds, str_class):
        # cmds = shlex.split(cmds)  # disable auto removing \ on windows
        cmds = cmds.split()
    else:
        cmds = list(cmds)
    return cmds


def get_std_encoding(stream):
    return getattr(stream, "encoding", None) or sys.getfilesystemencoding()


def reg_cleanup(func, *args, **kwargs):
    atexit.register(func, *args, **kwargs)


def on_method_ready(method_name):
    """Wrapper for lazy initialize some instance method."""
    def wrapper(func):
        @wraps(func)
        def ready_func(inst, *args, **kwargs):
            key = "_%s_ready" % method_name
            if not getattr(inst, key, None):
                method = getattr(inst, method_name)
                method()
                setattr(inst, key, True)
            return func(inst, *args, **kwargs)
        return ready_func
    return wrapper