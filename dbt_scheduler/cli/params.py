import typer

daemon_mode = typer.Option(
    False,
    "--daemon",
    help="Daemonize instead of running in the foreground",
)
