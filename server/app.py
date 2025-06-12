#!/usr/bin/env python3

from flask import Flask, jsonify, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)


# Route: Get earthquake by ID
@app.route('/earthquakes/<int:id>')
def get_earthquake_by_id(id):
    quake = Earthquake.query.filter_by(id=id).first()

    if quake:
        response = make_response(jsonify(quake.to_dict()), 200)
    else:
        response = make_response(
            jsonify({'message': f"Earthquake {id} not found."}), 404
        )
    
    return response


# Route: Get earthquakes by minimum magnitude
@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    quake_list = [quake.to_dict() for quake in quakes]

    response = make_response(
        jsonify({
            "count": len(quake_list),
            "quakes": quake_list
        }),
        200
    )

    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)

