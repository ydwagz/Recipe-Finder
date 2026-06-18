from flask_wtf import FlaskForm
from wtforms.fields import (
    DateField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
)
from wtforms.validators import DataRequired, equal_to, length
from flask_wtf.file import FileAllowed, FileField, FileSize


class LoginForm(FlaskForm):
    username = StringField("Enter Username", validators=[DataRequired()])
    password = PasswordField("Enter Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    image = FileField(validators=[
        FileSize(1024 * 1024 * 3, message="Photo must be smaller than 3MB"),
        FileAllowed(["png", "jpg", "jpeg"]),
    ])
    username = StringField("Enter Username", validators=[
        DataRequired()
    ])
    password = PasswordField("Enter Password", validators=[
        DataRequired(),
        length(min=6, max=24),
    ])
    confirm_password = PasswordField("Confirm Password", validators=[
        DataRequired(),
        equal_to("password", message="Passwords do not match"),
    ])
    birthdate = DateField()
    country = SelectField(choices=["Choose Country", "Georgia", "USA", "Japan"])

    register = SubmitField("Register")


class RecipeForm(FlaskForm):
    image = FileField("Upload recipe photo")
    title = StringField("Enter Recipe Title", validators=[DataRequired()])
    ingredients = StringField("Enter Recipe Ingredients", validators=[DataRequired()])

    submit = SubmitField("Save Recipe")
