from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import current_user

from app.extensions import db
from app.forms import CheckoutForm
from app.models import Category, Product, Order, OrderItem

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    categories = Category.query.order_by(Category.name).all()
    query = request.args.get("q", "", type=str).strip()
    selected_category = request.args.get("category", "", type=str)

    products_query = Product.query
    if selected_category:
        products_query = products_query.join(Category).filter(Category.slug == selected_category)
    if query:
        products_query = products_query.filter(Product.name.ilike(f"%{query}%"))

    products = products_query.order_by(Product.created_at.desc()).all()
    return render_template("shop/index.html", products=products, categories=categories, selected_category=selected_category, search_query=query)


@main_bp.route("/category/<slug>")
def category_page(slug):
    category = Category.query.filter_by(slug=slug).first_or_404()
    products = Product.query.filter_by(category_id=category.id).all()
    return render_template("shop/category.html", category=category, products=products)


@main_bp.route("/product/<slug>")
def product_detail(slug):
    product = Product.query.filter_by(slug=slug).first_or_404()
    return render_template("shop/product_detail.html", product=product)


@main_bp.route("/cart")
def cart():
    cart = session.get("cart", {})
    product_ids = list(cart.keys())
    products = Product.query.filter(Product.id.in_(product_ids)).all() if product_ids else []
    cart_items = []
    total = 0.0

    for product in products:
        quantity = int(cart.get(str(product.id), 0))
        if quantity > 0:
            subtotal = product.price * quantity
            total += subtotal
            cart_items.append({"product": product, "quantity": quantity, "subtotal": subtotal})

    return render_template("shop/cart.html", cart_items=cart_items, total=total)


@main_bp.route("/cart/add/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    cart = session.get("cart", {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    session["cart"] = cart
    flash(f"{product.name} added to cart.", "success")
    return redirect(url_for("main.product_detail", slug=product.slug))


@main_bp.route("/cart/update/<int:product_id>", methods=["POST"])
def update_cart(product_id):
    quantity = int(request.form.get("quantity", 1))
    cart = session.get("cart", {})
    if quantity <= 0:
        cart.pop(str(product_id), None)
    else:
        cart[str(product_id)] = quantity
    session["cart"] = cart
    flash("Cart updated.", "info")
    return redirect(url_for("main.cart"))


@main_bp.route("/cart/remove/<int:product_id>", methods=["POST"])
def remove_from_cart(product_id):
    cart = session.get("cart", {})
    cart.pop(str(product_id), None)
    session["cart"] = cart
    flash("Item removed from cart.", "info")
    return redirect(url_for("main.cart"))


@main_bp.route("/checkout", methods=["GET", "POST"])
def checkout():
    cart = session.get("cart", {})
    if not cart:
        flash("Your cart is empty.", "warning")
        return redirect(url_for("main.home"))

    cart_items = []
    total = 0.0
    for product_id, quantity in cart.items():
        product = Product.query.get(product_id)
        if not product:
            continue
        quantity = int(quantity)
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({"product": product, "quantity": quantity, "subtotal": subtotal})

    form = CheckoutForm()
    if form.validate_on_submit():
        order = Order(
            user_id=current_user.id if current_user.is_authenticated else None,
            customer_name=form.customer_name.data,
            email=form.email.data,
            address=form.address.data,
            total=total,
        )
        db.session.add(order)
        db.session.flush()

        for item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item["product"].id,
                quantity=item["quantity"],
                price_at_purchase=item["product"].price,
            )
            db.session.add(order_item)
            item["product"].stock = max(item["product"].stock - item["quantity"], 0)

        db.session.commit()
        session["cart"] = {}
        flash("Your order has been placed successfully.", "success")
        return redirect(url_for("main.account_orders"))

    return render_template("shop/checkout.html", form=form, cart_items=cart_items, total=total)


@main_bp.route("/account/orders")
def account_orders():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))

    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template("account/orders.html", orders=orders)
