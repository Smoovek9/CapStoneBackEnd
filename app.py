from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

app = Flask(__name__)
cors = CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class DemonSlayer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False)
    rank = db.Column(db.String(144), unique=False)
    swordType = db.Column(db.String(158), unique=False)
    url = db.Column(db.String(168), unique=False)

    def __init__(self, name, rank, swordType, url):
        self.name = name
        self.rank = rank
        self.swordType = swordType
        self.url = url


class DemonSlayerSchema(ma.Schema):
    class Meta:
        fields = ('id','name', 'rank', 'swordType', 'url')


demonSlayer_schema = DemonSlayerSchema()
demonSlayers_schema = DemonSlayerSchema(many=True)

# Endpoint to create a new guide
@app.route('/demonSlayer', methods=["POST"])
def add_demonSlayer():
    name = request.json['name']
    rank = request.json['rank']
    swordType = request.json['swordType']
    url = request.json['url']


    new_demonSlayer = DemonSlayer(name, rank, swordType, url)

    db.session.add(new_demonSlayer)
    db.session.commit()

    demonSlayer = DemonSlayer.query.get(new_demonSlayer.id)

    return demonSlayer_schema.jsonify(demonSlayer)

# Endpoint to query all guides
@app.route("/demonSlayers", methods=["GET"])
def get_demonSlayers():
    all_demonSlayers = DemonSlayer.query.all()
    result = demonSlayers_schema.dump(all_demonSlayers)
    return jsonify(result)


# Endpoint to querying a single guide
@app.route("/demonSlayer/<id>", methods =["GET"])
def get_demonSlayer(id):
    demonSlayer = DemonSlayer.query.get(id)
    return demonSlayer_schema.jsonify(demonSlayer)

# Endpoint for updating a guide
@app.route("/demonSlayer/<id>", methods=["PUT"])
def demonSlayer_update(id):
    demonSlayer = DemonSlayer.query.get(id)
    name = request.json['name']
    rank = request.json['rank']
    swordType = request.json['swordType']
    url = request.json['url']

    demonSlayer.name = name
    demonSlayer.rank = rank
    demonSlayer.swordType = swordType
    demonSlayer.url = swordType

    db.session.commit()
    return demonSlayer_schema.jsonify(demonSlayer)

# Endpoint for deleting a record
@app.route("/demonSlayer/<id>", methods=["DELETE"])
def demonSlayer_delete(id):
    demonSlayer = DemonSlayer.query.get(int(id))
    db.session.delete(demonSlayer)
    db.session.commit()

    return "DemonSlayer was successfully deleted!"


if __name__ == '__main__':
    app.run(debug=True)
