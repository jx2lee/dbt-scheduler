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
    dbt_scheduler_home = expand_env_var(os.environ.get('DBT_SCHEDULER_HOME', '~/dbt-scheduler'))
    
    if not os.path.exists(dbt_scheduler_home):
        os.makedirs(dbt_scheduler_home, mode=0o755, exist_ok=True)
            
    return dbt_scheduler_home


DBT_SCHEDULER_HOME = get_dbt_scheduler_home()
