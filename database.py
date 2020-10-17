# database
from flask import Flask, render_template, redirect, url_for, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import pymysql
import relations

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://test:password@152.3.52.135/test1'

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)
User = (2, 1)  # dummy user who is placeholder until we make login

"""Functions for the main page"""


@app.route('/')
def main():
    result = db.session.query(relations.Item.sku, relations.Item.title, relations.Item.category, relations.Item.price,
                              relations.Item.rating).all()
    return jsonify(result)  # TODO: send this to GUI for display


"""Functions for the items"""


@app.route('/item/<sku>', methods=["GET"])
def item_page(sku):
    result = db.session.query(relations.Item.sku, relations.Item.title, relations.Item.category, relations.Item.price,
                              relations.Item.rating, relations.Item.description).filter(relations.Item.sku == sku)
    return jsonify(result)  # TODO: send this to GUI for display


@app.route("/addItem", methods=["POST"])
def add_item():
    return redirect(url_for('root'))


@app.route("/removeItem")
def remove_item():
    print(msg)
    return redirect(url_for('root'))


@app.route("/displayCategory")
def display_category():
    placetaker = ''
    return render_template('displayCategory.html', placetaker=placetaker)


@app.route("/productDescription", methods=['GET', 'POST'])
def product_description():
    placetaker = ''
    return render_template("productDescription.html", placetaker=placetaker)


"""Functions for search results"""


@app.route('/results', methods=['GET', 'POST'])
def search_results(search):
    result = db.session.query(relations.Item.sku, relations.Item.title, relations.Item.category, relations.Item.price,
                              relations.Item.rating, relations.Item.description).filter(relations.Item.title == search)
    # return render_template('result.html', placetaker =placetaker) TODO: send this to GUI for display


"""Functions for the cart"""


@app.route('/<id>/cart')
def cart_page(sku):
    result = db.session.query(relations.Item.sku, relations.Item.title, relations.Item.category, relations.Item.price,
                              relations.Item.rating, relations.Item.description).filter(relations.Item.sku == sku)
    return result  # TODO: send this to GUI for display


@app.route("/addToCart")
def add_to_cart():
    print('')
    return redirect(url_for('root'))


@app.route("/removeFromCart")
def remove_from_cart():
    return redirect(url_for('root'))


"""Functions for the user profile"""


@app.route('/<user_id>/profile', methods=["GET"])
def profile_page(user_id):
    result = db.session.query(relations.User.id, relations.User.is_buyer, relations.User.password,
                              relations.User.email, relations.User.question, relations.User.answer,
                              relations.User.address).filter(relations.User.id == user_id)
    return jsonify(result)  # TODO: send this to GUI for display


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
    print(db.session.query(relations.User.id, relations.User.is_buyer).all())
