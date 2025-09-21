from flask import Flask, request, jsonify
from models import db, Restaurant, Pizza, RestaurantPizza
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# ---- ROUTES ----

@app.route("/restaurants", methods=["GET"])
def get_restaurants():
    restaurants = db.session.query(Restaurant).all()
    return jsonify([r.to_dict() for r in restaurants]), 200

@app.route("/restaurants/<int:id>", methods=["GET"])
def get_restaurant(id):
    restaurant = db.session.get(Restaurant, id)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404
    return jsonify(restaurant.to_dict_with_pizzas()), 200

@app.route("/restaurants/<int:id>", methods=["DELETE"])
def delete_restaurant(id):
    restaurant = db.session.get(Restaurant, id)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404
    db.session.delete(restaurant)
    db.session.commit()
    return jsonify({}), 204

@app.route("/pizzas", methods=["GET"])
def get_pizzas():
    pizzas = db.session.query(Pizza).all()
    return jsonify([p.to_dict() for p in pizzas]), 200

@app.route("/restaurant_pizzas", methods=["POST"])
def create_restaurant_pizza():
    data = request.get_json()
    errors = []

    # Validate price
    price = data.get("price")
    if not isinstance(price, int) or not (1 <= price <= 30):
        errors.append("validation errors")

    # Validate IDs
    restaurant = Restaurant.query.get(data.get("restaurant_id"))
    pizza = Pizza.query.get(data.get("pizza_id"))
    if not restaurant or not pizza:
        errors.append("validation errors")

    if errors:
        return jsonify({"errors": errors}), 400

    try:
        rp = RestaurantPizza(
            restaurant_id=data["restaurant_id"],
            pizza_id=data["pizza_id"],
            price=price
        )
        db.session.add(rp)
        db.session.commit()
        return jsonify(rp.to_dict()), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"errors": ["validation errors"]}), 400
