#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod:
    process_log_entry

:Synopsis:

:Author:
    servilla

:Created:
    8/18/24
"""
from datetime import datetime
import os
from pathlib import Path
from zipfile import BadZipFile

import daiquiri

import compressor
from config import Config
import mimemail

logger = daiquiri.getLogger(__name__)


def process(log_name: str, log_entry: dict, compress: bool) -> bool:
    file = log_entry["file"]
    compression = log_entry["compression"]
    email = log_entry["email"]

    logfile = Path(file)
    if logfile.is_file() and os.access(logfile, os.R_OK):
        if compress:
            try:
                logfile = compressor.compress(logfile, compression)
            except BadZipFile as e:
                logger.error(e)
                return False
        for name in email:
            address = email[name]
            subject = f"{Config.HOST}: {logfile.name}"
            message = f"Sending {logfile.name} from {Config.HOST} on {datetime.now().isoformat()}"
            mimemail.send_mail(subject, message, name, address, logfile)
            logger.info(f"Sending {log_name}: {str(logfile)} to {name} at {address}")
        if compress and logfile.exists():
            os.remove(logfile)
    else:
        logger.error(str(logfile) + " does not exist or read-access denied")
        return False
    return True