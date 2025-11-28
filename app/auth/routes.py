from flask import (
    Blueprint,
    render_template,
    request,
    session,
    redirect,
    url_for,
)
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db
from ..models import Usuario

auth_bp = Blueprint("auth", __name__)
# Mini backend de autenticación


# Ruta de registro
@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    error = None
    if request.method == "POST":
        nombre = request.form.get("nombre")
        email = request.form.get("email")
        password = request.form.get("password")

        if not nombre or not email or not password:
            error = "Por favor, complete todos los campos."
        elif Usuario.query.filter_by(email=email).first():
            error = "El correo ya está registrado."
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
            return redirect(url_for("auth.login"))

    return render_template("registro.html", error=error)


# Ruta de login
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if email == "" or password == "":
            error = "Por favor, complete todos los campos."
        else:
            usuario = Usuario.query.filter_by(email=email).first()
            if usuario and check_password_hash(usuario.password, password):
                session["usuario_id"] = usuario.id
                session["usuario_nombre"] = usuario.nombre
                return redirect(url_for("main.panel"))
            else:
                error = "Credenciales inválidas. Intente de nuevo."

    return render_template("login.html", error=error)


# Ruta de logout
@auth_bp.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
