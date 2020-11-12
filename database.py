# database
from flask import Flask, render_template, redirect, url_for, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os
import pymysql
from werkzeug.datastructures import MultiDict

import relations
from forms import AddItemForm, EditProfileForm

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://test:password@152.3.52.135/test1'

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)
User = {'id': 1, 'is_seller': 0}    # dummy user who is placeholder until we make login


"""Functions for the main page"""


@app.route('/')
def main():
    result = list()
    query = db.session.query(relations.Item.sku, relations.Item.title, relations.Item.category, relations.Item.price,
                             relations.Item.rating, relations.Item.seller, relations.Item.image).all()

    for row in query:
        temp = {'sku': row.sku, 'title': row.title, 'category': row.category, 'price': row.price,
                'rating': row.rating, 'seller': row.seller, 'image': row.image}
        result.append(temp)

    return render_template('index.html', items=result, user=1)


"""Functions for the items"""


@app.route('/item/<sku>', methods=["GET"])
def item_page(sku):
    query = db.session.query(relations.Item.sku, relations.Item.title, relations.Item.category, relations.Item.price,
                             relations.Item.rating, relations.Item.description, relations.Item.seller,
                             relations.Item.image).filter(relations.Item.sku == sku)
    query = query[0]
    item = {'sku': query.sku, 'title': query.title, 'category': query.category, 'price': query.price,
            'rating': query.rating, 'description': query.description, 'seller': query.seller,
            'image': query.image}
    return render_template('item.html', items=item)


@app.route("/addItem", methods=['GET', 'POST'])
def add_item():
    form = AddItemForm()
    if request.method == 'POST':
        print("Add Item Form Validated")
        new_item = relations.Item(sku=form.sku.data, title=form.title.data, description=form.description.data,
                                  price=form.price.data, category=form.category.data, quantity=form.quantity.data,
                                  rating=0, seller=form.seller.data, image=form.image.data)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('main'))
    return render_template('additem.html', form=form)


@app.route("/removeItem", methods=["GET", "POST"])
def remove_item():
    sku = request.get_json()
    item = db.session.query(relations.Item).filterby(sku=sku["sku"])
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('main'))


@app.route("/displayCategories")
def display_categories():
    result = list()
    categories = db.session.query(relations.Category.name)
    for row in categories:
        temp = {'category': row.category}
        result.append(temp)
    return jsonify(result)


"""Functions for search results"""


@app.route('/<search>/results', methods=['GET', 'POST'])
def search_results(search):
    result = list()
    query = db.session.query(relations.Item.sku, relations.Item.title, relations.Item.category, relations.Item.price,
                             relations.Item.rating, relations.Item.description).filter(relations.Item.title == search)
    for row in query:
        temp = {'sku': row.sku, 'title': row.title, 'category': row.category, 'price': row.price,
                'rating': row.rating, 'description': row.description}
        result.append(temp)
    return jsonify(result)


"""Functions for the cart"""


@app.route('/<buyer_id>/cart')
def cart_page(buyer_id):
    result = list()
    query = db.session.query(relations.Cart.buyer_id, relations.Cart.sku).filter(relations.Cart.buyer_id == buyer_id)
    for row in query:
        item_query = db.session.query(relations.Item.sku, relations.Item.title, relations.Item.category,
                                      relations.Item.price,
                                      relations.Item.rating, relations.Item.description, relations.Item.seller,
                                      relations.Item.image).filter(relations.Item.sku == row.sku)
        item_query = item_query[0]
        item = {'sku': item_query.sku, 'title': item_query.title, 'category': item_query.category,
                'price': item_query.price, 'rating': item_query.rating, 'description': item_query.description,
                'seller': item_query.seller, 'image': item_query.image}
        result.append(item)
    return render_template('cart.html', items=result, user=1)


@app.route("/addToCart", methods=["GET", "POST"])
def add_to_cart():
    if request.method == 'POST':
        sku = request.form['sku']
        buyer_id = 1     # request.form['buyer_id']
        new_item = relations.Cart(sku=sku, buyer_id=buyer_id)
        db.session.add(new_item)
        db.session.commit()
    return redirect(url_for('main'))


@app.route("/removeFromCart", methods=["POST"])
def remove_from_cart():                                           # THIS DOES NOT YET WORK !!!!!!!
    buyer_id = 1  # request.form["buyer_id"]
    sku = request.form["sku"]
    # relations.Cart.delete_from_cart(sku, buyer_id)
    item = db.session.query(relations.Cart).filter(relations.Cart.sku == sku, relations.Cart.buyer_id == buyer_id)
    db.session.delete(item)
    db.session.commit()
    return redirect('/'+str(buyer_id)+'/cart')   # Change the 1 to be a buyer_id variable


""" Functions for checkout """
@app.route("/<user_id>/checkout", methods=["GET", "POST"])
def checkout(user_id):
    # Address query
    address_query = db.session.query(relations.User.address).filter(relations.User.id == user_id).first()
    address = {'address': address_query.address}
    # Cart query
    cart_result = list()
    cart_query = db.session.query(relations.Cart.buyer_id,
                                  relations.Cart.sku).filter(relations.Cart.buyer_id == user_id)
    for row in cart_query:
        item_query = db.session.query(relations.Item.sku, relations.Item.title, relations.Item.category,
                                      relations.Item.price,
                                      relations.Item.rating, relations.Item.description, relations.Item.seller,
                                      relations.Item.image).filter(relations.Item.sku == row.sku)
        item_query = item_query[0]
        item = {'sku': item_query.sku, 'title': item_query.title, 'category': item_query.category,
                'price': item_query.price, 'rating': item_query.rating, 'description': item_query.description,
                'seller': item_query.seller, 'image': item_query.image}
        cart_result.append(item)
    return render_template('checkout.html', address=address, cart=cart_result)




"""Functions for the user profile"""


@app.route('/<user_id>/profile', methods=["GET"])
def profile_page(user_id):
    query = db.session.query(relations.User.id, relations.User.is_seller, relations.User.password,
                             relations.User.email, relations.User.question, relations.User.answer,
                             relations.User.address).filter(relations.User.id == user_id).first()
    user = {'id': query.id, 'is_seller': query.is_seller, 'password': query.password,
              'email': query.email, 'question': query.question, 'answer': query.answer,
              'address': query.address}
    return render_template('user_profile.html', user=user)


@app.route("/<user_id>/profile/edit", methods=["POST", "GET"])
def edit_profile(user_id):
    query = db.session.query(relations.User.password,
                             relations.User.email, relations.User.question, relations.User.answer,
                             relations.User.address).filter(relations.User.id == user_id).first()
    user = {'password': query.password,
            'email': query.email, 'question': query.question, 'answer': query.answer,
            'address': query.address}
    if request.method == 'GET':
        form = EditProfileForm(formdata=MultiDict({'email': query.email, 'password': query.password, 'address': query.address, 'question': query.question, 'answer': query.answer}))
    elif request.method == 'POST':
        form = EditProfileForm()
        relations.User.updateUser(form.password.data, form.email.data, form.question.data, form.answer.data, form.address.data, user_id)
        print("Edit Profile Form Validated")
        #TODO: modify user and other relevant tables with new data input
        db.session.commit()
    return render_template('edit_profile.html', user=user, form=form)


@app.route("/account/profile/changePassword", methods=["GET", "POST"])
def change_password():
    in_dict = request.get_json()
    user = User.query.filter_by(id=in_dict["id"]).first()
    user.password = in_dict["password"]
    db.session.commit()
    return "Password successfully updated."


if __name__ == '__main__':
    app.run()
    #print(db.session.query(relations.User.id, relations.User.is_buyer).all())

