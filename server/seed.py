from app import app, db
from models import Restaurant, Pizza

with app.app_context():
    # Clear existing data
    db.drop_all()
    db.create_all()

    # --- Restaurants ---
    r1 = Restaurant(name="Pizza Palace", address="123 Main St")
    r2 = Restaurant(name="Cheesy Bites", address="456 Side Ave")
    r3 = Restaurant(name="Slice Heaven", address="789 Broadway Blvd")

    db.session.add_all([r1, r2, r3])

    # --- Pizzas ---
    p1 = Pizza(name="Margherita", ingredients="Tomato, Mozzarella, Basil")
    p2 = Pizza(name="Pepperoni", ingredients="Tomato, Mozzarella, Pepperoni")
    p3 = Pizza(name="Veggie Delight", ingredients="Tomato, Mozzarella, Peppers, Onions, Olives")

    db.session.add_all([p1, p2, p3])

    db.session.commit()
    print("Database seeded successfully!")
