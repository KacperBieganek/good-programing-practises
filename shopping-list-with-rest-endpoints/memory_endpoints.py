from typing import Dict, Type

from flask import request, jsonify, Blueprint
from flask_marshmallow import Marshmallow

memory_endpoints = Blueprint('memory_endpoints', __name__)
current_user_id = 0
current_order_id = 0
current_storage_id = 0
ma = Marshmallow()


class User:
    def __init__(self, user_id, firstname, secondname, password, login, role):
        self.user_id = user_id
        self.firstname = firstname
        self.secondname = secondname
        self.password = password
        self.login = login
        self.role = role


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('user_id', 'firstname', 'secondname', 'role')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class Order:
    def __init__(self, order_id, creationdate, plannedorderdate, item, amount, customerid):
        self.order_id = order_id
        self.creationdate = creationdate
        self.plannedorderdate = plannedorderdate
        self.item = item
        self.amount = amount
        self.customerid = customerid


class OrderSchema(ma.Schema):
    class Meta:
        fields = ('order_id', 'creationdate', 'plannedorderdate', 'realorderdate', 'item', 'amount', 'customerid')


order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)


class Storage:
    def __init__(self, storage_id, item, amount):
        self.storage_id = storage_id
        self.item = item
        self.amount = amount


class StorageSchema(ma.Schema):
    class Meta:
        fields = ('storage_id', 'item', 'amount')


storage_schema = StorageSchema()
many_storage_schema = StorageSchema(many=True)

user_dictionary: Dict[int, Type[User]] = {}
order_dictionary: Dict[int, Type[Order]] = {}
storage_dictionary: Dict[int, Type[Storage]] = {}


# endpoint to create new user
@memory_endpoints.route("/user", methods=["POST"])
def add_user():
    global current_user_id
    firstname = request.json['firstname']
    secondname = request.json['secondname']
    password = request.json['password']
    login = request.json['login']
    role = request.json['role']

    new_user = User(current_user_id, firstname, secondname, password, login, role)

    user_dictionary.update({current_user_id: new_user})
    current_user_id += 1

    return user_schema.jsonify(new_user)


# endpoint to show all users
@memory_endpoints.route("/user", methods=["GET"])
def get_user():
    all_users = user_dictionary.values()
    result = users_schema.dump(all_users)
    return jsonify(result.data)


# endpoint to get user detail by id
@memory_endpoints.route("/user/<id>", methods=["GET"])
def user_detail(id):
    user = user_dictionary.get(id)
    return user_schema.jsonify(user)


# endpoint to update user
@memory_endpoints.route("/user/<id>", methods=["PUT"])
def user_update(id):
    user = user_dictionary.get(id)
    username = request.json['username']
    email = request.json['email']

    user.email = email
    user.username = username

    user_dictionary.update({id: user})
    return user_schema.jsonify(user)


# endpoint to delete user
@memory_endpoints.route("/user/<id>", methods=["DELETE"])
def user_delete(id):
    user = user_dictionary.pop(id)

    return user_schema.jsonify(user)


# endpoint to create new order
@memory_endpoints.route("/order", methods=["POST"])
def add_order():
    global current_order_id
    firstname = request.json['firstname']
    secondname = request.json['secondname']
    password = request.json['password']
    login = request.json['login']
    role = request.json['role']

    new_order = Order(current_order_id, firstname, secondname, password, login, role)

    order_dictionary.update({current_order_id: new_order})
    current_order_id += 1

    return order_schema.jsonify(new_order)


# endpoint to show all orders
@memory_endpoints.route("/order", methods=["GET"])
def get_order():
    all_orders = order_dictionary.values()
    result = orders_schema.dump(all_orders)
    return jsonify(result.data)


# endpoint to get order detail by id
@memory_endpoints.route("/order/<id>", methods=["GET"])
def order_detail(id):
    order = order_dictionary.get(id)
    return order_schema.jsonify(order)


# endpoint to update order
@memory_endpoints.route("/order/<id>", methods=["PUT"])
def order_update(id):
    order = order_dictionary.get(id)
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

    order_dictionary.update({id: order})
    return order_schema.jsonify(order)


# endpoint to delete order
@memory_endpoints.route("/order/<id>", methods=["DELETE"])
def order_delete(id):
    order = order_dictionary.pop(id)

    return order_schema.jsonify(order)


# endpoint to create new storage
@memory_endpoints.route("/storage", methods=["POST"])
def add_storage():
    global current_storage_id
    item = request.json['item']
    amount = request.json['amount']

    new_storage = Storage(current_storage_id, item, amount)

    storage_dictionary.update({current_storage_id: new_storage})
    current_storage_id += 1

    return storage_schema.jsonify(new_storage)


# endpoint to show all storages
@memory_endpoints.route("/storage", methods=["GET"])
def get_storage():
    all_storage = storage_dictionary.values()
    result = many_storage_schema.dump(all_storage)
    return jsonify(result.data)


# endpoint to get storage detail by id
@memory_endpoints.route("/storage/<id>", methods=["GET"])
def storage_detail(id):
    storage = storage_dictionary.get(id)
    return storage_schema.jsonify(storage)


# endpoint to update storage
@memory_endpoints.route("/storage/<id>", methods=["PUT"])
def storage_update(id):
    storage = storage_dictionary.get(id)
    item = request.json['item']
    amount = request.json['amount']

    storage.item = item
    storage.amount = amount

    storage_dictionary.update({id: storage})
    return storage_schema.jsonify(storage)


# endpoint to delete storage
@memory_endpoints.route("/storage/<id>", methods=["DELETE"])
def storage_delete(id):
    storage = storage_dictionary.pop(id)

    return storage_schema.jsonify(storage)
