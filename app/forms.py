from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, SubmitField, FloatField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional, NumberRange


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match")],
    )
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class ProductForm(FlaskForm):
    name = StringField("Product name", validators=[DataRequired(), Length(min=2, max=150)])
    description = TextAreaField("Description", validators=[DataRequired(), Length(min=10, max=2000)])
    price = FloatField("Price", validators=[DataRequired(), NumberRange(min=0.01)])
    stock = IntegerField("Stock", validators=[DataRequired(), NumberRange(min=0)])
    image_url = StringField("Image URL", validators=[Optional(), Length(max=500)])
    category_id = SelectField("Category", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Save product")


class CheckoutForm(FlaskForm):
    customer_name = StringField("Full name", validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    address = TextAreaField("Address", validators=[DataRequired(), Length(min=10, max=800)])
    submit = SubmitField("Place order")
