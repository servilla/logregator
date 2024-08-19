#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: __init__

:Synopsis:

:Author:
    servilla

:Created:
    2/6/22
"""
import logging
import pathlib
import sys

import daiquiri


cwd = pathlib.Path(".").resolve()
logfile = cwd / "tests.log"
daiquiri.setup(level=logging.INFO,
               outputs=(daiquiri.output.File(str(logfile)), "stdout",))
logger = daiquiri.getLogger(__name__)

src = pathlib.Path(cwd).parent / "src/logregator"
sys.path.insert(0, str(src))
