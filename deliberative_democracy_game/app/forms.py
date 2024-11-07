# app/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    character_name = StringField("Character Name", validators=[DataRequired()])
    submit = SubmitField("Login")


class ProjectInsightForm(FlaskForm):
    insight = TextAreaField("Your Insight", validators=[DataRequired()])
    submit = SubmitField("Submit")
