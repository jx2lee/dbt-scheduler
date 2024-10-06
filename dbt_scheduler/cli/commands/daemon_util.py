import signal
from typing import Callable, Optional

import typer
from daemon import daemon
from daemon.pidfile import TimeoutPIDLockFile

from dbt_scheduler.cli.cli_utils import setup_locations, sigint_handler, sigquit_handler
from dbt_scheduler.utils.process_util import check_if_pidfile_process_is_running


def run_daemon(
    #TODO: daemon_mode ~ log_file 까지 optional argument 로 변경하기
    *,
    args: typer.Context,
    process_name: str,
    callback: Callable,
    umask: str = "0o022",
    pid_file: Optional[str] = None,
):
    if args.params.get("daemon"):
        pid = pid_file or args.params.get("pid") if pid_file is not None or args.params.get("pid") is not None else None
        pid, stdout, stderr, log_file = setup_locations(
            process=process_name, pid=pid, stdout=args.params.get("stdout"), stderr=args.params.get("stderr"), log=args.params.get("log_file")
        )
        pid, stdout, stderr, log_file = setup_locations(
            process=process_name,
            pid=pid_file,
            stdout=stdout,
            stderr=stderr,
            log=log_file,
        )

        check_if_pidfile_process_is_running(pid_file=pid, process_name=process_name)

        with open(stdout, "a") as stdout_handle, open(stderr, "a") as stderr_handle:
            stdout_handle.truncate(0)
            stderr_handle.truncate(0)

            ctx = daemon.DaemonContext(
                pidfile=TimeoutPIDLockFile(pid, -1),
                stdout=stdout_handle,
                stderr=stderr_handle,
                umask=int(umask, 8),
            )

            with ctx:
                callback()
    else:
        signal.signal(signal.SIGINT, sigint_handler)
        signal.signal(signal.SIGTERM, sigint_handler)
        signal.signal(signal.SIGQUIT, sigquit_handler)
        callback()
