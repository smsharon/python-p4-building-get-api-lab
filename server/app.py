#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from sqlalchemy import desc

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = []
    for bakery in Bakery.query.all():
        bakery_dict = {
            "id": bakery.id,
            "name": bakery.name,
            "created_at": bakery.created_at,
        }
        bakeries.append(bakery_dict )

    response = make_response(
        jsonify(bakeries),
        200
    )
    response.headers["Content-Type"] = "application/json"
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()

    bakery_dict = bakery.to_dict()

    response = make_response(
        jsonify(bakery_dict),
        200
    )
    response.headers["Content-Type"] = "application/json"

    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = []
    for baked_goods in BakedGood.query.order_by(desc(BakedGood.price)).all():
        baked_goods_dict = {
            "id": baked_goods.id,
            "name": baked_goods.name,
            "price": baked_goods.price,
            "created_at": baked_goods.created_at,
        }
        baked_goods_by_price.append(baked_goods_dict )

    response = make_response(
        jsonify(baked_goods_by_price),
        200
    )
    response.headers["Content-Type"] = "application/json"
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive_baked_good = BakedGood.query.order_by(desc(BakedGood.price)).first()
    
    baked_goods_dict = {
            "id": most_expensive_baked_good.id,
            "name": most_expensive_baked_good.name,
            "price": most_expensive_baked_good.price,
            "created_at": most_expensive_baked_good.created_at,
        }
        

    response = make_response(
        jsonify(baked_goods_dict ),
        200
    )
    response.headers["Content-Type"] = "application/json"
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
