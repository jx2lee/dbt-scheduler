import os


def expand_env_var(env_var: str | None) -> str | None:
    if not env_var:
        return env_var
    while True:
        interpolated = os.path.expanduser(os.path.expandvars(str(env_var)))
        if interpolated == env_var:
            return interpolated
        else:
            env_var = interpolated


def get_dbt_scheduler_home():
    return expand_env_var(os.environ.get('DBT_SCHEDULER_HOME', '~/dbt-scheduler'))


DBT_SCHEDULER_HOME = get_dbt_scheduler_home()
