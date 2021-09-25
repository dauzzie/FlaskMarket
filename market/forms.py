from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError, NumberRange
from market.models import User
from market.item_service import generate_barcode


class RegisterForm(FlaskForm):
    
    # this naming convention is very specific, must be validate_<field>
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')
    
    def validate_email(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email address already exists! Please try a different email address')


    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Register')

class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Login')

class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase Item')

class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell Item')

class AddItemForm(FlaskForm):
    name = StringField(label='Product Name:', validators=[Length(min=5), DataRequired()])
    description = StringField(label='Description:', validators=[Length(max=150)])
    price = IntegerField(label='Price: ', validators=[NumberRange(min=0, max=9999999)])
    barcode = StringField(label='Barcode: ', validators=[Length(min=12, max=12)], default=generate_barcode())
    submit = SubmitField(label='Add Item')

