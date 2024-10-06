import time

import typer

from dbt_scheduler import settings
from dbt_scheduler.cli.commands.daemon_util import run_daemon


def _run_scheduler_job():
    while True:
        print(time.time())
        time.sleep(5)
    pass

def run(
    daemon: bool = typer.Option(False, "--daemon", help="Daemonize instead of running in the foreground"),
    log_file: str = typer.Option(None, "--log-file", help="Location of the log file", metavar="LOG_FILE"),
    pid: str = typer.Option(default=None, help="PID file location", metavar="PID"),
    stderr: str = typer.Option(default=None, help="Redirect stderr to this file", metavar="STDERR"),
    stdout: str = typer.Option(default=None, help="Redirect stdout to this file", metavar="STDOUT"),
    ctx: typer.Context = typer.Option(None),
):
    """
    Run a dbt scheduler instance
    """
    print(settings.HEADER)

    run_daemon(
        args=ctx,
        process_name="scheduler",
        callback=lambda: _run_scheduler_job(),
    )
