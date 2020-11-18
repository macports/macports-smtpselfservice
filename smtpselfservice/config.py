"""
Module containing the configuration options for this Flask application.
"""
# SPDX-License-Identifier: BSD-2-Clause

import os
import secrets


class Config:  # pylint: disable=too-few-public-methods
    """
    Wrapper object for configuration options
    """

    SECRET_KEY = os.environ.get("SECRET_KEY") or secrets.token_bytes(64)
    DATABASE_URI = (
        os.environ.get("DATABASE_URI") or "postgresql://localhost/smtpselfservice"
    )
    PREFERRED_EMAIL_DOMAIN = os.environ.get("PREFERRED_EMAIL_DOMAIN") or "macports.org"
