# database
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import pymysql
import relations


SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://test:password@152.3.52.135/test1'

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)
User = {'id': 1, 'is_buyer': 0} #dummy user who is placeholder until we make login

"""Functions for the main page"""
@app.route('/')
@app.route('/main')
def mainPage():
    result = db.session.query(relations.Item.sku, relations.Item.title, relations.Item.category, relations.Item.price, relations.Item.rating).all()
    return result #TODO: send this to GUI for display

"""Functions for the items"""
@app.route('/item/<sku>')
def itemPage(sku):
    result = db.session.query(relations.Item.sku, relations.Item.title, relations.Item.category, relations.Item.price,
                              relations.Item.rating, relations.Item.description).filter(relations.Item.sku == sku)
    return result #TODO: send this to GUI for display

@app.route("/addItem", methods=["GET", "POST"])
def addItem():
    item_dict = request.get_json()
    new_item = relations.Item(title = item_dict['title'], description = item_dict['description'], price = item_dict['price'],
                              category = item_dict['category'], seller = User['id']) #TODO: get info from GUI and create exception if user tries to add same item multiple times, randomly generate sku
    db.session.add(new_item)
    db.session.commit()
    return redirect(url_for('main'))

@app.route("/removeItem", methods=["GET", "POST"])
def removeItem():
    sku = request.get_json()
    item = db.session.query(relations.Item).filterby(sku = sku["sku"])
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('main'))

@app.route("/displayCategory")
def displayCategory():
    placetaker = ''
    return render_template('displayCategory.html', placetaker =placetaker)

@app.route("/productDescription", methods=['GET', 'POST'])
def productDescription():
    placetaker = ''
    return render_template("productDescription.html", placetaker =placetaker)

"""Functions for search results"""
@app.route('/results', methods=['GET', 'POST'])
def search_results(search):
    result = db.session.query(relations.Item.sku, relations.Item.title, relations.Item.category, relations.Item.price,
                              relations.Item.rating, relations.Item.description).filter(relations.Item.title == search)
    #return render_template('result.html', placetaker =placetaker) TODO: send this to GUI for display

"""Functions for the cart"""
@app.route('/<id>/cart')
def cartPage(sku):
    result = db.session.query(relations.Item.sku, relations.Item.title, relations.Item.category, relations.Item.price, relations.Item.rating, relations.Item.description).filter(relations.Item.sku == sku)
    return result #TODO: send this to GUI for display

@app.route("/addToCart")
def addToCart():
    print('')
    return redirect(url_for('root'))

@app.route("/removeFromCart")
def removeFromCart():

    return redirect(url_for('root'))

"""Functions for the user profile"""
@app.route('/<id>/profile')
def profilePage(sku):
    result = db.session.query(relations.Item.sku, relations.Item.title, relations.Item.category, relations.Item.price, relations.Item.rating, relations.Item.description).filter(relations.Item.sku == sku)
    return result #TODO: send this to GUI for display

@app.route("/account/profile/edit")
def editProfile():
    placetaker = ''
    return render_template("editProfile.html", placetaker =placetaker)

@app.route("/account/profile/changePassword", methods=["GET", "POST"])
def changePassword():
    placetaker = ''
    return render_template("changePassword.html", placetaker =placetaker)

@app.route("/updateProfile", methods=["GET", "POST"])
def updateProfile():
    return redirect(url_for('editProfile'))

if __name__ == '__main__':
    app.run()
    print(db.session.query(relations.User.id, relations.User.is_buyer).all())

