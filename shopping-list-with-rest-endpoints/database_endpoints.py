from flask import request, jsonify, Blueprint
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

db_endpoints = Blueprint('db_endpoints', __name__)
db = SQLAlchemy()
ma = Marshmallow()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(40))
    secondname = db.Column(db.String(40))
    password = db.Column(db.String(100))
    login = db.Column(db.String(40), unique=True)
    role = db.Column(db.String(40))

    def __init__(self, firstname, secondname, password, login, role):
        self.firstname = firstname
        self.secondname = secondname
        self.password = password
        self.login = login
        self.role = role


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('firstname', 'secondname', 'role')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    creationdate = db.Column(db.String(10))
    plannedorderdate = db.Column(db.String(10))
    realorderdate = db.Column(db.String(10))
    item = db.Column(db.String(40))
    amount = db.Column(db.Integer)
    customerid = db.Column(db.Integer, ForeignKey("user.id"), nullable=False)

    def __init__(self, creationdate, plannedorderdate, item, amount, customerid):
        self.creationdate = creationdate
        self.plannedorderdate = plannedorderdate
        self.item = item
        self.amount = amount
        self.customerid = customerid


class OrderSchema(ma.Schema):
    class Meta:
        fields = ('id', 'creationdate', 'plannedorderdate', 'realorderdate', 'item', 'amount', 'customerid')


order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)


class Storage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(50))
    amount = db.Column(db.Integer)

    def __init__(self, item, amount):
        self.item = item
        self.amount = amount


class StorageSchema(ma.Schema):
    class Meta:
        fields = ('id', 'item', 'amount')


storage_schema = StorageSchema()
many_storage_schema = StorageSchema(many=True)


# endpoint to create new user
@db_endpoints.route("/user", methods=["POST"])
def add_user():
    firstname = request.json['firstname']
    secondname = request.json['secondname']
    password = request.json['password']
    login = request.json['login']
    role = request.json['role']

    new_user = User(firstname, secondname, password, login, role)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)


# endpoint to show all users
@db_endpoints.route("/user", methods=["GET"])
def get_user():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result.data)


# endpoint to get user detail by id
@db_endpoints.route("/user/<id>", methods=["GET"])
def user_detail(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)


# endpoint to update user
@db_endpoints.route("/user/<id>", methods=["PUT"])
def user_update(id):
    user = User.query.get(id)
    username = request.json['username']
    email = request.json['email']

    user.email = email
    user.username = username

    db.session.commit()
    return user_schema.jsonify(user)


# endpoint to delete user
@db_endpoints.route("/user/<id>", methods=["DELETE"])
def user_delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)


# endpoint to create new order
@db_endpoints.route("/order", methods=["POST"])
def add_order():
    firstname = request.json['firstname']
    secondname = request.json['secondname']
    password = request.json['password']
    login = request.json['login']
    role = request.json['role']

    new_order = Order(firstname, secondname, password, login, role)

    db.session.add(new_order)
    db.session.commit()

    return order_schema.jsonify(new_order)


# endpoint to show all orders
@db_endpoints.route("/order", methods=["GET"])
def get_order():
    all_orders = Order.query.all()
    result = orders_schema.dump(all_orders)
    return jsonify(result.data)


# endpoint to get order detail by id
@db_endpoints.route("/order/<id>", methods=["GET"])
def order_detail(id):
    order = Order.query.get(id)
    return order_schema.jsonify(order)


# endpoint to update order
@db_endpoints.route("/order/<id>", methods=["PUT"])
def order_update(id):
    order = Order.query.get(id)
    creationdate = request.json['creationdate']
    plannedorderdate = request.json['plannedorderdate']
    realorderdate = request.json['realorderdate']
    item = request.json['item']
    amount = request.json['amount']
    customerid = request.json['customerid']

    order.creationdate = creationdate
    order.plannedorderdate = plannedorderdate
    order.realorderdate = realorderdate
    order.item = item
    order.amount = amount
    order.customerid = customerid

    db.session.commit()
    return order_schema.jsonify(order)


# endpoint to delete order
@db_endpoints.route("/order/<id>", methods=["DELETE"])
def order_delete(id):
    order = Order.query.get(id)
    db.session.delete(order)
    db.session.commit()

    return order_schema.jsonify(order)


# endpoint to create new storage
@db_endpoints.route("/storage", methods=["POST"])
def add_storage():
    item = request.json['item']
    amount = request.json['amount']

    new_storage = Storage(item, amount)

    db.session.add(new_storage)
    db.session.commit()

    return storage_schema.jsonify(new_storage)


# endpoint to show all storages
@db_endpoints.route("/storage", methods=["GET"])
def get_storage():
    all_storage = Storage.query.all()
    result = many_storage_schema.dump(all_storage)
    return jsonify(result.data)


# endpoint to get storage detail by id
@db_endpoints.route("/storage/<id>", methods=["GET"])
def storage_detail(id):
    storage = Storage.query.get(id)
    return storage_schema.jsonify(storage)


# endpoint to update storage
@db_endpoints.route("/storage/<id>", methods=["PUT"])
def storage_update(id):
    storage = Storage.query.get(id)
    item = request.json['item']
    amount = request.json['amount']

    storage.item = item
    storage.amount = amount

    db.session.commit()
    return storage_schema.jsonify(storage)


# endpoint to delete storage
@db_endpoints.route("/storage/<id>", methods=["DELETE"])
def storage_delete(id):
    storage = Storage.query.get(id)
    db.session.delete(storage)
    db.session.commit()

    return storage_schema.jsonify(storage)
