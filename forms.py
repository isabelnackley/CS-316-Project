from flask_wtf import FlaskForm
from wtforms import StringField, TextField, IntegerField, DecimalField, SubmitField, HiddenField, SelectField
from wtforms.validators import DataRequired


class AddItemForm(FlaskForm):
    """Form to add a new item to the database"""
    sku = IntegerField('SKU', [DataRequired()])
    title = TextField('Title', [DataRequired()])
    description = TextField('Description', [DataRequired()])
    category = StringField('Category', [DataRequired()])
    quantity = IntegerField('Quantity', [DataRequired()])
    price = DecimalField('Price', [DataRequired()], places=2)
    seller = IntegerField('Seller', [DataRequired()])
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
    star_rating = IntegerField('Star Rating', [DataRequired()])
    written_rating = TextField('Written Review')
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    email = StringField('Email', [DataRequired()])
    password = StringField('Password', [DataRequired()])
    submit = SubmitField('Log In')

