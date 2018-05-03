from flask import Flask
from flask_marshmallow import Marshmallow

import database_endpoints
import files_endpoints
import memory_endpoints
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')
database_endpoints.db.init_app(app)
database_endpoints.ma.init_app(Marshmallow(app))
memory_endpoints.ma.init_app(Marshmallow(app))
files_endpoints.ma.init_app(Marshmallow(app))
with app.app_context():
    database_endpoints.db.create_all()
app.register_blueprint(database_endpoints.db_endpoints, url_prefix='/database')
app.register_blueprint(memory_endpoints.memory_endpoints, url_prefix='/memory')
app.register_blueprint(files_endpoints.files_endpoints, url_prefix='/files')

if __name__ == '__main__':
    app.run(debug=True)
