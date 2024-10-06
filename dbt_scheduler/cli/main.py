import typer

from dbt_scheduler.cli.commands.run_command import run
from dbt_scheduler.cli.commands.status_command import status

app = typer.Typer(
    #TODO: enable set using environment.
    add_completion=False,
    no_args_is_help=True,
    rich_markup_mode=None,
    pretty_exceptions_enable=False,
)
app.command()(run)
app.command()(status)


@app.callback()
def callback():
    #TODO: main command callback.
    """
    """
