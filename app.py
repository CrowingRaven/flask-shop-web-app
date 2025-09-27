from flask import Flask, render_template, request, make_response
import json
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from ShopDataBase import *

class basketForm(FlaskForm):
    amount = StringField("Amount to add to cart: ", validators=[DataRequired(), Length(min=1, max=10)])
    submit = SubmitField("Submit")

class cardDetailsForm(FlaskForm):
    card_name = StringField("Name on Card", validators=[DataRequired(), Length(min=1, max=50, message="Name on card must be between 1 and 50 characters")])
    card_number = StringField("Card Number", validators=[DataRequired(), Length(min=16, max=16, message="Card number must be exactly 16 digits")])
    card_expiry = StringField("Expiry Date (MM/YY)", validators=[DataRequired(), Length(min=5, max=5, message="Expiry date must be in MM/YY format")])
    card_cvc = StringField("CVC", validators=[DataRequired(), Length(min=3, max=3, message="CVC must be exactly 3 digits")])
    email = StringField("Email", validators=[DataRequired() ,Length(min=1, max=50)])
    submit = SubmitField("Submit")
    
@app.route('/')
def galleryPage():
    sort = request.args.get('sort', 'name')
    if sort == 'price':
        hardware = Hardware.query.order_by(Hardware.price).all()
    elif sort == 'impact':
        hardware = Hardware.query.order_by(Hardware.impact).all()
    else:
        hardware = Hardware.query.order_by(Hardware.name).all()
    return render_template('index.html', hardware=hardware, sort=sort)

@app.route('/hard/<int:hardId>', methods=["GET", "POST"])
def singleProductPage(hardId):
    form = basketForm()
    hardware_item = Hardware.query.get(hardId)  # Fetch the hardware item by its ID
    if form.validate_on_submit():
        basket = request.cookies.get('basket', '')
        basket_items = basket.split(',') if basket else []
        basket_items.append(f"{hardId}:{form.amount.data}")
        response = make_response(render_template('SingleTechBasket.html', hardware=hardware_item, num=form.amount.data))
        response.set_cookie('basket', ','.join(basket_items))
        return response
    else:
        return render_template('SingleTech.html', hardware=hardware_item, form=form)
    
@app.route('/basket', methods=["GET", "POST"])
def basketPage():
    basket = request.cookies.get('basket', '')
    basket_items = basket.split(',') if basket else []
    items = []
    total_price = 0
    for item in basket_items:
        hardId, amount = item.split(':')
        hardware_item = Hardware.query.get(int(hardId))
        items.append((hardware_item, int(amount)))
        total_price += hardware_item.price * int(amount)
    total_price = round(total_price, 2)
    return render_template('basket.html', items=items, total_price=total_price)

@app.route('/remove/<int:hardId>', methods=["POST"])
def removeFromBasket(hardId):
    basket = request.cookies.get('basket', '')
    basket_items = basket.split(',') if basket else []
    updated_basket = [item for item in basket_items if not item.startswith(f"{hardId}:")]
    items = []
    total_price = 0
    for item in updated_basket:
        hardId, amount = item.split(':')
        hardware_item = Hardware.query.get(int(hardId))
        items.append((hardware_item, int(amount)))
        total_price += hardware_item.price * int(amount)
    total_price = round(total_price, 2)
    response = make_response(render_template('basket.html', items=items, total_price=total_price))
    response.set_cookie('basket', ','.join(updated_basket))
    return response

@app.route('/checkout', methods=['GET', 'POST'])
def checkoutPage():
    form = cardDetailsForm()
    basket = request.cookies.get('basket', '')
    basket_items = basket.split(',') if basket else []
    items = []
    total_price = 0
    for item in basket_items:
        hardId, amount = item.split(':')
        hardware_item = Hardware.query.get(int(hardId))
        items.append({
            'name': hardware_item.name,
            'price': hardware_item.price,
            'quantity': int(amount),
            'total': hardware_item.price * int(amount)
        })
        total_price += hardware_item.price * int(amount)
    total_price = round(total_price, 2)

    if form.validate_on_submit():
        response = make_response(render_template('succesfulCheckout.html', email=form.email.data))
        response.set_cookie('basket', '', expires=0)  # Clear the basket
        return response
    return render_template('checkout.html', form=form, items=items, total_price=total_price)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
