"""
A Flask webapp to allow setting a password in a database.
"""
# SPDX-License-Identifier: BSD-2-Clause
from flask import Flask, flash, url_for, redirect, render_template, request

from passlib.hash import argon2

import diceware
import psycopg

from smtpselfservice.config import Config
from smtpselfservice.forms import PasswordForm
from smtpselfservice.github import GitHubApiError, get_user

app = Flask(__name__)
app.config.from_object(Config)


@app.route("/", methods=["GET", "POST"])
def home():
    """
    Return the form required to change the password, or change it when invoked
    with POST.
    """
    form = PasswordForm()
    if form.validate_on_submit():
        password = f"{{ARGON2ID}}{argon2.hash(form.password.data)}"

        try:
            username, domain = get_user(
                request.headers.get("X-Forwarded-Access-Token"),
                app.config["PREFERRED_EMAIL_DOMAIN"],
            )
            # pylint: disable=not-context-manager
            with psycopg.connect(app.config["DATABASE_URI"]) as conn:
                with conn.cursor() as cur:
                    with conn.transaction():
                        cur.execute(
                            """
                            INSERT INTO
                                users (username, domain, password)
                            VALUES
                                (%s, %s, %s)
                            ON CONFLICT (username, domain) DO UPDATE
                                SET password = excluded.password
                            """,
                            (username, domain, password),
                        )
            flash("Password successfully changed.", "success")
            return redirect(url_for("settings"))
        except psycopg.Error as psycopge:
            flash(f"Error updating password: {psycopge!s}", "danger")
        except GitHubApiError as githube:
            flash(f"Error determining your email address: {githube!s}", "danger")

        return redirect(url_for("home"))

    dicewares = []
    for _ in range(5):
        dicewares.append(diceware.get_passphrase())
    return render_template("home.html", form=form, dicewares=dicewares)


@app.route("/settings", methods=["GET", "POST"])
def settings():
    """
    Show details about the settings to configure in the mailclient.
    """
    return render_template("settings.html", title="Settings")
