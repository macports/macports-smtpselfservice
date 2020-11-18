"""
Forms used for setting the password.
"""
from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class PasswordForm(FlaskForm):
    """
    The WTForm to change the password
    """

    password = PasswordField(
        "New Password",
        description="The new SMTP password for your user.",
        validators=[DataRequired(), Length(min=12)],
    )
    submit = SubmitField("Change Password")
