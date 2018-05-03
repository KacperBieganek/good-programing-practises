from flask import request, jsonify, Blueprint
from flask_marshmallow import Marshmallow
import threading
import csv

files_endpoints = Blueprint('files_endpoints', __name__)
current_user_id = 0
current_order_id = 0
current_storage_id = 0
user_lock = threading.Lock()
order_lock = threading.Lock()
storage_lock = threading.Lock()
user_file = 'resources/user.csv'
order_file = 'resources/order.csv'
storage_file = 'resources/storage.csv'

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


# endpoint to create new user
@files_endpoints.route("/user", methods=["POST"])
def add_user():
    global current_user_id
    firstname = request.json['firstname']
    secondname = request.json['secondname']
    password = request.json['password']
    login = request.json['login']
    role = request.json['role']

    new_user = User(current_user_id, firstname, secondname, password, login, role)

    with user_lock:
        with open(user_file, mode="a") as uf:
            writer = csv.writer(uf)
            members = [attr for attr in dir(new_user) if
                       not callable(getattr(new_user, attr)) and not attr.startswith("__")]
            writer.writerow(members)
    current_user_id += 1

    return user_schema.jsonify(new_user)


# endpoint to show all users
@files_endpoints.route("/user", methods=["GET"])
def get_user():
    all_users = []
    with user_lock:
        with open(user_file, 'r') as uf:
            reader = csv.reader(uf)
            for row in reader:
                all_users.append(User(row[0], row[1], row[2], row[3], row[4], row[5]))

    result = users_schema.dump(all_users)
    return jsonify(result.data)


# endpoint to get user detail by id
@files_endpoints.route("/user/<id>", methods=["GET"])
def user_detail(id):
    user = None

    with user_lock:
        with open(user_file, 'r') as uf:
            reader = csv.reader(uf)
            for row in reader:
                if row[0] == id:
                    user = User(row[0], row[1], row[2], row[3], row[4], row[5])

    return user_schema.jsonify(user)


# endpoint to update user
@files_endpoints.route("/user/<id>", methods=["PUT"])
def user_update(id):
    user = None

    with user_lock:
        with open(user_file, 'wr') as uf:
            reader = csv.reader(uf)
            for row in reader:
                if row[0] == id:
                    user = User(row[0], row[1], row[2], row[3], row[4], row[5])
            username = request.json['username']
            email = request.json['email']
            user.email = email
            user.username = username
            writer = csv.writer(uf)
            for row in reader:
                if row[0] == id:
                    members = [attr for attr in dir(user) if
                               not callable(getattr(user, attr)) and not attr.startswith("__")]
                    writer.writerow(members)
                else:
                    writer.writerow(row)

    return user_schema.jsonify(user)


# endpoint to delete user
@files_endpoints.route("/user/<id>", methods=["DELETE"])
def user_delete(id):
    user = None

    with user_lock:
        with open(user_file, 'wr') as uf:
            reader = csv.reader(uf)
            writer = csv.writer(uf)
            for row in reader:
                if row[0] == id:
                    user = User(row[0], row[1], row[2], row[3], row[4], row[5])
                else:
                    writer.writerow(row)

    return user_schema.jsonify(user)


# endpoint to create new order
@files_endpoints.route("/order", methods=["POST"])
def add_order():
    global current_order_id
    firstname = request.json['firstname']
    secondname = request.json['secondname']
    password = request.json['password']
    login = request.json['login']
    role = request.json['role']

    new_order = Order(current_order_id, firstname, secondname, password, login, role)

    with order_lock:
        with open(order_file, mode="a") as uf:
            writer = csv.writer(uf)
            members = [attr for attr in dir(new_order) if
                       not callable(getattr(new_order, attr)) and not attr.startswith("__")]
            writer.writerow(members)
    current_order_id += 1

    return order_schema.jsonify(new_order)


# endpoint to show all orders
@files_endpoints.route("/order", methods=["GET"])
def get_order():
    all_orders = []
    with order_lock:
        with open(order_file, 'r') as uf:
            reader = csv.reader(uf)
            for row in reader:
                all_orders.append(Order(row[0], row[1], row[2], row[3], row[4], row[5]))

    result = orders_schema.dump(all_orders)
    return jsonify(result.data)


# endpoint to get order detail by id
@files_endpoints.route("/order/<id>", methods=["GET"])
def order_detail(id):
    order = None

    with order_lock:
        with open(order_file, 'r') as uf:
            reader = csv.reader(uf)
            for row in reader:
                if row[0] == id:
                    order = Order(row[0], row[1], row[2], row[3], row[4], row[5])

    return order_schema.jsonify(order)


# endpoint to update order
@files_endpoints.route("/order/<id>", methods=["PUT"])
def order_update(id):
    order = None
    with order_lock:
        with open(order_file, 'wr') as uf:
            reader = csv.reader(uf)
            for row in reader:
                if row[0] == id:
                    order = order(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
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
            writer = csv.writer(uf)
            for row in reader:
                if row[0] == id:
                    members = [attr for attr in dir(order) if
                               not callable(getattr(order, attr)) and not attr.startswith("__")]
                    writer.writerow(members)
                else:
                    writer.writerow(row)

    return order_schema.jsonify(order)


# endpoint to delete order
@files_endpoints.route("/order/<id>", methods=["DELETE"])
def order_delete(id):
    order = None

    with order_lock:
        with open(order_file, 'wr') as uf:
            reader = csv.reader(uf)
            writer = csv.writer(uf)
            for row in reader:
                if row[0] == id:
                    order = Order(row[0], row[1], row[2], row[3], row[4], row[5])
                else:
                    writer.writerow(row)

    return order_schema.jsonify(order)


# endpoint to create new storage
@files_endpoints.route("/storage", methods=["POST"])
def add_storage():
    global current_storage_id
    item = request.json['item']
    amount = request.json['amount']

    new_storage = Storage(current_storage_id, item, amount)

    with storage_lock:
        with open(storage_file, mode="a") as uf:
            writer = csv.writer(uf)
            members = [attr for attr in dir(new_storage) if
                       not callable(getattr(new_storage, attr)) and not attr.startswith("__")]
            writer.writerow(members)
    current_storage_id += 1

    return storage_schema.jsonify(new_storage)


# endpoint to show all storages
@files_endpoints.route("/storage", methods=["GET"])
def get_storage():
    all_storage = []
    with storage_lock:
        with open(storage_file, 'r') as uf:
            reader = csv.reader(uf)
            for row in reader:
                all_storage.append(Storage(row[0], row[1], row[2]))
    result = many_storage_schema.dump(all_storage)
    return jsonify(result.data)


# endpoint to get storage detail by id
@files_endpoints.route("/storage/<id>", methods=["GET"])
def storage_detail(id):
    storage = None

    with storage_lock:
        with open(storage_file, 'r') as uf:
            reader = csv.reader(uf)
            for row in reader:
                if row[0] == id:
                    storage = Storage(row[0], row[1], row[2])

    return storage_schema.jsonify(storage)


# endpoint to update storage
@files_endpoints.route("/storage/<id>", methods=["PUT"])
def storage_update(id):
    storage = None
    with storage_lock:
        with open(storage_file, 'wr') as uf:
            reader = csv.reader(uf)
            for row in reader:
                if row[0] == id:
                    storage = Storage(row[0], row[1], row[2])
            item = request.json['item']
            amount = request.json['amount']

            storage.item = item
            storage.amount = amount
            writer = csv.writer(uf)
            for row in reader:
                if row[0] == id:
                    members = [attr for attr in dir(storage) if
                               not callable(getattr(storage, attr)) and not attr.startswith("__")]
                    writer.writerow(members)
                else:
                    writer.writerow(row)

    return storage_schema.jsonify(storage)


# endpoint to delete storage
@files_endpoints.route("/storage/<id>", methods=["DELETE"])
def storage_delete(id):
    storage = None

    with storage_lock:
        with open(storage_file, 'wr') as uf:
            reader = csv.reader(uf)
            writer = csv.writer(uf)
            for row in reader:
                if row[0] == id:
                    storage = Storage(row[0], row[1], row[2])
                else:
                    writer.writerow(row)

    return storage_schema.jsonify(storage)
