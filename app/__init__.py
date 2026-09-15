import os
from pathlib import Path

from flask import Flask, session
from flask_login import current_user
from dotenv import load_dotenv
from sqlalchemy import inspect
from sqlalchemy.engine.url import make_url

from app.extensions import db, login_manager, bcrypt, migrate
from app.config import Config

load_dotenv()


def reset_sqlite_if_needed(app):
    database_url = app.config.get("SQLALCHEMY_DATABASE_URI", "")
    if not database_url.startswith("sqlite"):
        return

    db_url = make_url(database_url)
    sqlite_file = Path(db_url.database or "")
    if not sqlite_file.is_absolute():
        sqlite_file = (Path(__file__).resolve().parent.parent / sqlite_file).resolve()

    if not sqlite_file.exists():
        return

    try:
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        if "users" in tables and "role" not in inspector.get_columns("users"):
            sqlite_file.unlink()
    except Exception:
        sqlite_file.unlink()


def seed_database():
    from app.models import User, Category, Product

    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password = os.getenv("ADMIN_PASSWORD")
    if admin_email and admin_password:
        admin = User.query.filter_by(email=admin_email).first()
        if not admin:
            admin = User(username="admin", email=admin_email, role="admin")
            admin.password = admin_password
            db.session.add(admin)

    if Category.query.count() == 0:
        categories = [
            Category(name="Electronics", slug="electronics"),
            Category(name="Fashion", slug="fashion"),
            Category(name="Home", slug="home"),
            Category(name="Sports", slug="sports"),
        ]
        db.session.add_all(categories)

    if Product.query.count() == 0:
        categories_by_name = {category.name: category for category in Category.query.all()}
        products = [
            Product(
                name="Wireless Headphones",
                slug="wireless-headphones",
                description="High-quality wireless headphones with noise cancellation and deep bass.",
                price=129.99,
                stock=25,
                image_url="https://images.unsplash.com/photo-1546435770-a3e426bf472b?auto=format&fit=crop&w=900&q=80",
                category_id=categories_by_name["Electronics"].id,
            ),
            Product(
                name="Modern Smart Watch",
                slug="modern-smart-watch",
                description="Track your activity, heart rate, and notifications in one stylish device.",
                price=199.99,
                stock=18,
                image_url="https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=900&q=80",
                category_id=categories_by_name["Electronics"].id,
            ),
            Product(
                name="Classic Leather Jacket",
                slug="classic-leather-jacket",
                description="Premium fit jacket made for everyday comfort and style.",
                price=149.99,
                stock=12,
                image_url="https://images.unsplash.com/photo-1551028719-00167b16eac5?auto=format&fit=crop&w=900&q=80",
                category_id=categories_by_name["Fashion"].id,
            ),
            Product(
                name="Minimal Desk Lamp",
                slug="minimal-desk-lamp",
                description="Elegant lighting solution for bedrooms, offices, and creative spaces.",
                price=59.99,
                stock=30,
                image_url="https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=900&q=80",
                category_id=categories_by_name["Home"].id,
            ),
            Product(
                name="Yoga Mat Pro",
                slug="yoga-mat-pro",
                description="Extra-thick cushioned mat designed for balance, stretching, and recovery.",
                price=39.99,
                stock=40,
                image_url="https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=900&q=80",
                category_id=categories_by_name["Sports"].id,
            ),
            Product(
                name="Travel Backpack",
                slug="travel-backpack",
                description="Water resistant backpack with multiple compartments and ergonomic design.",
                price=89.99,
                stock=22,
                image_url="https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=900&q=80",
                category_id=categories_by_name["Sports"].id,
            ),
        ]
        db.session.add_all(products)

    existing_image_updates = {
        "classic-leather-jacket": "https://images.unsplash.com/photo-1551028719-00167b16eac5?auto=format&fit=crop&w=900&q=80",
        "travel-backpack": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=900&q=80",
    }
    for slug, image_url in existing_image_updates.items():
        product = Product.query.filter_by(slug=slug).first()
        if product:
            product.image_url = image_url

    db.session.commit()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"

    from app.models import User, Category, Product
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    from app.routes.main import main_bp

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    @app.context_processor
    def inject_cart_context():
        cart = session.get("cart", {})
        cart_count = sum(int(quantity) for quantity in cart.values())
        return {
            "cart_count": cart_count,
            "is_admin_user": current_user.is_authenticated and current_user.role == "admin",
        }

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)

    with app.app_context():
        reset_sqlite_if_needed(app)
        db.create_all()
        seed_database()

    return app
