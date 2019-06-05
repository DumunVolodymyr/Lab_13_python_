from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Camping(db.Model):
    id = db.Column(db.Integer,  nullable=False,  primary_key=True, autoincrement=True)
    weight = db.Column(db.Integer, nullable=False, unique=False)
    price = db.Column(db.Integer, nullable=False, unique=False)
    producerName = db.Column(db.String(70), nullable=False, unique=False)

    def __init__(self, weight, price, producerName):
        self.weight = weight
        self.price = price
        self.producerName = producerName


class CampingSchema(ma.Schema):
    class Meta:
        fields = ('weight', 'price', 'producerName')


camping_schema = CampingSchema()
campings_schema = CampingSchema(many=True)
db.create_all()


@app.route("/camping", methods=["POST"])
def add_camping():
    weight = request.json['weight']
    price = request.json['price']
    producerName = request.json['producerName']

    new_camping = Camping(weight, price, producerName)

    db.session.add(new_camping)
    db.session.commit()

    return camping_schema.jsonify(new_camping)


@app.route("/camping", methods=["GET"])
def get_camping():
    all_campings = Camping.query.all()
    result = campings_schema.dump(all_campings)
    return jsonify(result.data)


@app.route("/camping/<id>", methods=["GET"])
def camping_detail(id):
    camping = Camping.query.get(id)
    return camping_schema.jsonify(camping)


@app.route("/camping/<id>", methods=["PUT"])
def camping_update(id):
    camping = Camping.query.get(id)
    weight = request.json['weight']
    price = request.json['price']
    producerName = request.json['producerName']

    camping.weight = weight
    camping.price = price
    camping.producerName = producerName

    db.session.commit()
    return camping_schema.jsonify(camping)


@app.route("/camping/<id>", methods=["DELETE"])
def camping_delete(id):
    camping = Camping.query.get(id)
    db.session.delete(camping)
    db.session.commit()

    return camping_schema.jsonify(camping)


if __name__ == '__main__':
    app.run()
