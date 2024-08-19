#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod:
    compressor

:Synopsis:

:Author:
    servilla

:Created:
    8/18/24
"""
import gzip
import shutil
from pathlib import Path
import zipfile

import daiquiri


logger = daiquiri.getLogger(__name__)


def compress(logfile: Path, compression: str) -> Path:
    if compression == "zip":
        compressed = Path(f"/tmp/{logfile.name}.zip")
        with zipfile.ZipFile(logfile, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(compressed)
    elif compression == "gzip":
        compressed = Path(f"/tmp/{logfile.name}.gz")
        with open(logfile, "rb") as f:
            with gzip.open(compressed, "wb") as gzipf:
                shutil.copyfileobj(f, gzipf)
    else:
        raise ValueError(f"{compression} is not supported")
    return compressed
