from flask_wtf import FlaskForm
from wtforms import StringField, TextField, IntegerField, DecimalField, SubmitField, HiddenField
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




