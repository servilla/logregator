#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: mimemail

:Synopsis:
    Provide MIME Multipart email support (see: https://realpython.com/python-send-email/)

:Author:
    servilla

:Created:
    4/3/22
"""
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from email import encoders
import smtplib
from pathlib import Path

import daiquiri

from config import Config


logger = daiquiri.getLogger(__name__)


def send_mail(subject: str, msg: str, to_name: str, to: str, attachment: Path = None) -> bool:

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = formataddr((Config.FROM_NAME, Config.FROM))
    message["To"] = formataddr((to_name, to))
    message.add_header("X-SES-CONFIGURATION-SET", "edi-dedicated")
    message.attach(MIMEText(msg, "plain"))

    with open(attachment, "rb") as file:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={attachment.name}")
        message.attach(part)

    try:
        with smtplib.SMTP(Config.RELAY_HOST, Config.RELAY_TLS_PORT) as server:
            server.starttls()
            server.login(Config.RELAY_USER, Config.RELAY_PASSWORD)
            server.sendmail(Config.FROM,to, message.as_string())
            server.quit()
        return True
    except Exception as e:
        logger.error(e)
        return False
