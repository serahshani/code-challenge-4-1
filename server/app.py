#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Hero, Power, HeroPower
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

# Define the Hero resource
class HeroResource(Resource):
    def get(self, hero_id=None):
        if hero_id is None:
            heroes = Hero.query.all()
            return jsonify([hero.to_dict() for hero in heroes])
        
        hero = Hero.query.get(hero_id)
        if hero:
            return jsonify(hero.to_dict())
        return make_response(jsonify({"error": "Hero not found"}), 404)

    def post(self):
        data = request.get_json()
        new_hero = Hero(**data)
        db.session.add(new_hero)
        db.session.commit()
        return make_response(jsonify(new_hero.to_dict()), 201)

    def patch(self, hero_id):
        hero = Hero.query.get(hero_id)
        if not hero:
            return make_response(jsonify({"error": "Hero not found"}), 404)
        
        data = request.get_json()
        for key, value in data.items():
            setattr(hero, key, value)
        db.session.commit()
        return jsonify(hero.to_dict())

# Define the Power resource
class PowerResource(Resource):
    def get(self, power_id=None):
        if power_id is None:
            powers = Power.query.all()
            return jsonify([power.to_dict() for power in powers])
        
        power = Power.query.get(power_id)
        if power:
            return jsonify(power.to_dict())
        return make_response(jsonify({"error": "Power not found"}), 404)

    def post(self):
        data = request.get_json()
        new_power = Power(**data)
        db.session.add(new_power)
        db.session.commit()
        return make_response(jsonify(new_power.to_dict()), 201)

    def patch(self, power_id):
        power = Power.query.get(power_id)
        if not power:
            return make_response(jsonify({"error": "Power not found"}), 404)
        
        data = request.get_json()
        for key, value in data.items():
            setattr(power, key, value)
        db.session.commit()
        return jsonify(power.to_dict())

# Define the HeroPower resource
class HeroPowerResource(Resource):
    def post(self):
        data = request.get_json()
        strength = data.get('strength')
        if strength not in ['Strong', 'Weak', 'Average']:
            return make_response(jsonify({"errors": ["validation errors"]}), 400)
        
        hero_id = data['hero_id']
        power_id = data['power_id']
        
        hero_power = HeroPower(hero_id=hero_id, power_id=power_id, strength=strength)
        db.session.add(hero_power)
        db.session.commit()
        return make_response(jsonify(hero_power.to_dict()), 201)

# Add routes for the resources
api.add_resource(HeroResource, '/heroes', '/heroes/<int:hero_id>')
api.add_resource(PowerResource, '/powers', '/powers/<int:power_id>')
api.add_resource(HeroPowerResource, '/hero_powers')

if __name__ == '__main__':
    app.run()
