import logging
import os
import sys

from dbt_scheduler.configuration import DBT_SCHEDULER_HOME

log = logging.getLogger(__name__)

HEADER = "\n".join(
    [
        r"______________ _____                    ______      _________      ______",
        r"______  /__  /___  /_      ________________  /____________  /___  ____  /____________",
        r"_  __  /__  __ \  __/________  ___/  ___/_  __ \  _ \  __  /_  / / /_  /_  _ \_  ___/",
        r"/ /_/ / _  /_/ / /_ _/_____/(__  )/ /__ _  / / /  __/ /_/ / / /_/ /_  / /  __/  /",
        r"\__,_/  /_.___/\__/        /____/ \___/ /_/ /_/\___/\__,_/  \__,_/ /_/  \___//_/",
    ]
)

LOGGING_LEVEL = logging.INFO


def prepare_syspath():
    config_path = os.path.join(DBT_SCHEDULER_HOME, "config")
    if config_path not in sys.path:
        sys.path.append(config_path)
