from flask_wtf import FlaskForm
from wtforms import StringField, TextField, IntegerField, DecimalField, SubmitField, HiddenField, SelectField
from wtforms.validators import DataRequired


class AddItemForm(FlaskForm):
    """Form to add a new item to the database"""
    title = TextField('Title', [DataRequired()])
    description = TextField('Description', [DataRequired()])
    category = StringField('Category', [DataRequired()])
    quantity = IntegerField('Quantity', [DataRequired()])
    price = DecimalField('Price', [DataRequired()], places=2)
    image = StringField('Image')
    submit = SubmitField('Submit')


class EditProfileForm(FlaskForm):
    """Form to edit user profile"""
    email = TextField('Email', [DataRequired()])
    password = TextField('Password', [DataRequired()])
    address = TextField('Address', [DataRequired()])
    question = TextField('Secret Question', [DataRequired()])
    answer = TextField('Answer', [DataRequired()])
    submit = SubmitField('Submit')


class EditItemForm(FlaskForm):
    """Form to edit seller's item"""
    title = TextField('Title', [DataRequired()])
    description = TextField('Description', [DataRequired()])
    category = SelectField('Category', [DataRequired()])
    quantity = IntegerField('Quantity', [DataRequired()])
    price = DecimalField('Price', [DataRequired()])
    image = TextField('Image', [DataRequired()])
    submit = SubmitField('Submit')


class WriteReviewForm(FlaskForm):
    star_rating = SelectField('Star Rating', choices=['1','2','3','4','5'])
    written_rating = TextField('Written Review')
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    email = StringField('Email', [DataRequired()])
    password = StringField('Password', [DataRequired()])
    submit = SubmitField('Log In')


class ForgotPasswordForm(FlaskForm):
    answer = StringField('Answer', [DataRequired()])
    submit = SubmitField('Enter')


class VerifyEmailForm(FlaskForm):
    email = StringField('Email', [DataRequired()])
    submit = SubmitField('Enter')


class CreateProfileForm(FlaskForm):
    """Form to create user profile"""
    is_seller = SelectField('Would you like to sign up as a seller?', choices=['Yes', 'No'], validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    question = StringField('Secret Question', validators=[DataRequired()])
    answer = StringField('Answer', validators=[DataRequired()])
    address = StringField('Shipping Address', validators=[DataRequired()])
    submit = SubmitField('Submit')

class SearchItemsForm(FlaskForm):
    item = StringField('Search Items', [DataRequired()])
    submit = SubmitField('Search')

class AddPaymentMethodForm(FlaskForm):
    credit_card = IntegerField('Credit Card Number', [DataRequired()])
    address = StringField('Billing Address', [DataRequired()])
    submit = SubmitField('Submit')
