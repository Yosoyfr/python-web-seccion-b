from flask import Blueprint, render_template, session, redirect, url_for, request, flash

from .. import db
from ..models import Producto

main_bp = Blueprint("main", __name__)


# Ruta de panel
@main_bp.route("/panel", methods=["GET"])
def panel():
    if "usuario_id" in session:
        usuario_nombre = session["usuario_nombre"]
        return render_template("panel.html", usuario_nombre=usuario_nombre)
    else:
        return redirect(url_for("auth.login"))


# Ruta principal
@main_bp.route("/", methods=["GET"])
def index():
    return render_template("index.html")


# Ruta de productos
@main_bp.route("/productos", methods=["GET", "POST"])
def productos():
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        nombre = request.form.get("nombre")
        descripcion = request.form.get("descripcion")
        precio = request.form.get("precio")
        stock = request.form.get("stock")

        if not nombre or not precio:
            flash("El nombre y el precio son obligatorios.", "error")
        else:
            nuevo_producto = Producto(
                nombre=nombre,
                descripcion=descripcion,
                precio=float(precio),
                stock=int(stock) if stock else 0,
                usuario_id=session["usuario_id"],
            )
            db.session.add(nuevo_producto)
            db.session.commit()
            flash("Producto agregado exitosamente.", "success")
            return redirect(url_for("main.productos"))

    lista_productos = Producto.query.order_by(Producto.created_at.desc()).all()
    return render_template("productos.html", productos=lista_productos)
