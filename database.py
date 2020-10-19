# database
from flask import Flask, render_template, redirect, url_for, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os
import pymysql
import relations
from forms import AddItemForm


SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://test:password@152.3.52.135/test1'

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)
User = {'id': 1, 'is_buyer': 0}    # dummy user who is placeholder until we make login


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

    return render_template('index.html', items=result)


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
    result = db.session.query(relations.Cart.buyer_id, relations.Cart.sku).filter(relations.Cart.buyer_id == buyer_id)
    return jsonify(result)


@app.route("/addToCart", methods=["POST"])
def add_to_cart():
    # item_dict = request.get_json()
    # new_item = relations.Cart(buyer_id=item_dict["buyer_id"], sku=item_dict["sku"])
    # db.session.add(new_item)
    # db.session.commit()
    return redirect(url_for('main'))


@app.route("/removeFromCart", methods=["POST"])
def remove_from_cart():
    sku = request.get_json()
    item = db.session.query(relations.Cart).filterby(buyer_id=sku["buyer_id"], sku=sku["sku"])
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('root'))


"""Functions for the user profile"""


@app.route('/<user_id>/profile', methods=["GET"])
def profile_page(user_id):
    query = db.session.query(relations.User.id, relations.User.is_buyer, relations.User.password,
                             relations.User.email, relations.User.question, relations.User.answer,
                             relations.User.address).filter(relations.User.id == user_id)
    result = {'id': query.id, 'is_buyer': query.is_buyer, 'password': query.password,
              'email': query.email, 'question': query.question, 'answer': query.answer,
              'address': query.address}
    return jsonify(result)


@app.route("/account/profile/edit", methods=["POST"])
def edit_profile():
    in_dict = request.get_json()
    user = User.query.filter_by(id=in_dict["id"]).first()
    user.is_buyer = in_dict["is_buyer"]
    user.password = in_dict["password"]
    user.email = in_dict["email"]
    user.question = in_dict["question"]
    user.answer = in_dict["answer"]
    user.address = in_dict["address"]
    db.session.commit()
    return "Profile successfully updated."


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

