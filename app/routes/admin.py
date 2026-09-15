from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from app.extensions import db
from app.forms import ProductForm
from app.models import Category, Product, Order, OrderItem

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin")
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash("You do not have access to the admin panel.", "danger")
        return redirect(url_for("main.home"))

    products = Product.query.order_by(Product.created_at.desc()).all()
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(8).all()
    total_revenue = sum(order.total for order in Order.query.all())
    return render_template(
        "admin/dashboard.html",
        products=products,
        recent_orders=recent_orders,
        total_revenue=total_revenue,
        total_products=Product.query.count(),
        total_orders=Order.query.count(),
    )


@admin_bp.route("/admin/orders")
@login_required
def admin_orders():
    if not current_user.is_admin:
        flash("You do not have access to the admin panel.", "danger")
        return redirect(url_for("main.home"))

    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template("admin/orders.html", orders=orders)


@admin_bp.route("/admin/orders/<int:order_id>")
@login_required
def admin_order_detail(order_id):
    if not current_user.is_admin:
        flash("You do not have access to the admin panel.", "danger")
        return redirect(url_for("main.home"))

    order = Order.query.get_or_404(order_id)
    return render_template("admin/order_detail.html", order=order)


@admin_bp.route("/admin/products/new", methods=["GET", "POST"])
@login_required
def admin_new_product():
    if not current_user.is_admin:
        flash("You do not have access to the admin panel.", "danger")
        return redirect(url_for("main.home"))

    form = ProductForm()
    form.category_id.choices = [(category.id, category.name) for category in Category.query.order_by(Category.name).all()]

    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            slug=form.name.data.lower().replace(" ", "-") + "-" + str(Product.query.count() + 1),
            description=form.description.data,
            price=form.price.data,
            stock=form.stock.data,
            image_url=form.image_url.data or "https://images.unsplash.com/photo-1521572267360-ee0c2909d518",
            category_id=form.category_id.data,
        )
        db.session.add(product)
        db.session.commit()
        flash("Product created successfully.", "success")
        return redirect(url_for("admin.admin_dashboard"))

    return render_template("admin/product_form.html", form=form, title="Create product")


@admin_bp.route("/admin/products/<int:product_id>/edit", methods=["GET", "POST"])
@login_required
def admin_edit_product(product_id):
    if not current_user.is_admin:
        flash("You do not have access to the admin panel.", "danger")
        return redirect(url_for("main.home"))

    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)
    form.category_id.choices = [(category.id, category.name) for category in Category.query.order_by(Category.name).all()]

    if form.validate_on_submit():
        product.name = form.name.data
        product.slug = form.name.data.lower().replace(" ", "-")
        product.description = form.description.data
        product.price = form.price.data
        product.stock = form.stock.data
        product.image_url = form.image_url.data or product.image_url
        product.category_id = form.category_id.data
        db.session.commit()
        flash("Product updated successfully.", "success")
        return redirect(url_for("admin.admin_dashboard"))

    return render_template("admin/product_form.html", form=form, title="Edit product", product=product)


@admin_bp.route("/admin/products/<int:product_id>/delete", methods=["POST"])
@login_required
def admin_delete_product(product_id):
    if not current_user.is_admin:
        flash("You do not have access to the admin panel.", "danger")
        return redirect(url_for("main.home"))

    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted.", "info")
    return redirect(url_for("admin.admin_dashboard"))
