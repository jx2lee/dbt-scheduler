import psutil
from lockfile.pidlockfile import PIDLockFile

from dbt_scheduler.exceptions import DbtSchedulerException


def check_if_pidfile_process_is_running(pid_file: str, process_name: str):
    pid_lock_file = PIDLockFile(path=pid_file)

    if pid_lock_file.is_locked():
        pid = pid_lock_file.read_pid()
        if pid is None:
            return
        try:
            proc = psutil.Process(pid)
            if proc.is_running():
                raise DbtSchedulerException(f"The {process_name} is already running under PID {pid}.")
        except psutil.NoSuchProcess:
            # If process is dead remove the pidfile
            pid_lock_file.break_lock()
