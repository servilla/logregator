#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod:
    test_mimemail

:Synopsis:
    Pytest for test_mimemail

:Author:
    servilla

:Created:
    8/18/24
"""
from pathlib import Path

from mimemail import send_mail


def test_send_mail():
    subject = "Test email"
    msg = "This is a test email"
    to_name = "Servilla"
    to = "mark.servilla@gmail.com"
    attachment = Path("../README.md")
    assert send_mail(subject, msg, to_name, to, attachment) is True
