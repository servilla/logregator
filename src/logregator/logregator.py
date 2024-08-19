#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod:
    logregator

:Synopsis:

:Author:
    servilla

:Created:
    8/11/24
"""
import json
from json import JSONDecodeError
import logging
from pathlib import Path

import click
import daiquiri

from config import Config
import process_log_entry

CWD = Path(".").resolve().as_posix()
LOGFILE = CWD + "/logregator.log"
daiquiri.setup(
    level=logging.INFO,
    outputs=(
        daiquiri.output.File(LOGFILE),
        "stdout",
    ),
)
logger = daiquiri.getLogger(__name__)


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("config", nargs=1, required=True)
@click.option("-c", "--compress", is_flag=True, default=False, help="Compress using zip.")
def main (config: str, compress:bool):
    """
    Logregator: A log aggregator for system logs

    \b
        CONFIG: JSON configuration file for log agrgregation.
    """
    logregator_config = Path(config)
    try:
        with open(logregator_config, "r") as f:
            logregator_json = json.load(f)
    except (FileNotFoundError, JSONDecodeError, IsADirectoryError) as e:
        logger.error(e)
        exit(1)

    for log_name in logregator_json:
        log_entry = logregator_json[log_name]
        process_log_entry.process(log_name, log_entry, compress)


if __name__ == '__main__':
    main()
