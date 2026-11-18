from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, BooleanField, SelectField, PasswordField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=64)])
    password = PasswordField('Password', validators=[DataRequired()])

class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=128)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=1000)])
    price = DecimalField('Price', places=2, validators=[DataRequired(), NumberRange(min=0.01, max=100000)])
    category_id = SelectField('Category', coerce=int)
    is_available = BooleanField('Available', default=True)
