import os
import sys
import threading
import traceback
from functools import wraps

from dbt_scheduler import settings


def inject_param(func):
    def inner(*args, **kwargs):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # kwargs[func.__name__] = func(*args, **kwargs)
            return func(*args, **kwargs)

        return wrapper

    return inner


def setup_locations(process, pid=None, stdout=None, stderr=None, log=None):
    """Logging paths."""
    if not stderr:
        stderr = os.path.join(settings.DBT_SCHEDULER_HOME, f"dbt-{process}.err")
    if not stdout:
        stdout = os.path.join(settings.DBT_SCHEDULER_HOME, f"dbt-{process}.out")
    if not log:
        log = os.path.join(settings.DBT_SCHEDULER_HOME, f"dbt-{process}.log")

    if not pid:
        pid = os.path.join(settings.DBT_SCHEDULER_HOME, f"dbt-{process}.pid")
    else:
        pid = os.path.abspath(pid)

    return pid, stdout, stderr, log


def sigint_handler(sig, frame):
    """
    Return without error on SIGINT or SIGTERM signals in interactive command mode.

    e.g. CTRL+C or kill <PID>
    """
    sys.exit(0)


def sigquit_handler(sig, frame):
    """
    Help debug deadlocks by printing stacktraces when this gets a SIGQUIT.

    e.g. kill -s QUIT <PID> or CTRL+
    """
    print(f"Dumping stack traces for all threads in PID {os.getpid()}")
    id_to_name = {th.ident: th.name for th in threading.enumerate()}
    code = []
    for thread_id, stack in sys._current_frames().items():
        code.append(f"\n# Thread: {id_to_name.get(thread_id, '')}({thread_id})")
        for filename, line_number, name, line in traceback.extract_stack(stack):
            code.append(f'File: "{filename}", line {line_number}, in {name}')
            if line:
                code.append(f"  {line.strip()}")
    print("\n".join(code))
