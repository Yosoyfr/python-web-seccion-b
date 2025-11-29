from flask import (
    Blueprint,
    render_template,
    request,
    session,
    redirect,
    url_for,
    flash,
)
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db
from ..models import Usuario

auth_bp = Blueprint("auth", __name__)
# Mini backend de autenticación


# Ruta de registro
@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():

    if request.method == "POST":
        nombre = request.form.get("nombre")
        email = request.form.get("email")
        password = request.form.get("password")

        if not nombre or not email or not password:
            flash("Por favor, complete todos los campos.", "danger")
        elif Usuario.query.filter_by(email=email).first():
            flash("El correo ya está registrado.", "danger")
        else:
            # encriptar la contraseña antes de guardarla
            print("Password antes de hash:", password)
            hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
            print("Password después de hash:", hashed_password)
            nuevo_usuario = Usuario(
                nombre=nombre, email=email, password=hashed_password
            )
            db.session.add(nuevo_usuario)
            db.session.commit()
            flash("Registro exitoso. Por favor, inicia sesión.", "success")
            return redirect(url_for("auth.login"))

    return render_template("registro.html")


# Ruta de login
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if email == "" or password == "":
            flash("Por favor, complete todos los campos.", "danger")
        else:
            usuario = Usuario.query.filter_by(email=email).first()
            if usuario and check_password_hash(usuario.password, password):
                session["usuario_id"] = usuario.id
                session["usuario_nombre"] = usuario.nombre
                flash("Has iniciado sesión correctamente.", "success")
                return redirect(url_for("main.panel"))
            else:
                flash("Correo o contraseña incorrectos.", "danger")

    return render_template("login.html")


# Ruta de logout
@auth_bp.route("/logout", methods=["GET"])
def logout():
    session.clear()
    flash("Has cerrado sesión correctamente.", "success")
    return redirect(url_for("auth.login"))
