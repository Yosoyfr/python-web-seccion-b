from flask import (
    Flask,
    render_template,
    request,
    session,
    redirect,
    url_for,
    make_response,
)
from flask_sqlalchemy import SQLAlchemy

# Create a Flask application instance
app = Flask(__name__)
app.secret_key = "clave_super_secreta"  # Necesaria para manejar sesiones
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# Modelos de ejemplo
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"<Usuario {self.nombre}>"


# Crear la base de datos
with app.app_context():
    db.create_all()


# Ruta principal
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/usuarios", methods=["GET", "POST"])
def usuarios():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        email = request.form.get("email")
        nuevo_usuario = Usuario(nombre=nombre, email=email)
        db.session.add(nuevo_usuario)
        db.session.commit()
        return redirect(url_for("usuarios"))

    usuarios = Usuario.query.all()
    return render_template("usuarios.html", usuarios=usuarios)


##################################################################


# Ruta de perfil
@app.route("/perfil", methods=["GET"])
def perfil():
    return render_template("perfil.html", user=user_data)


# Ruta de productos
@app.route("/productos", methods=["GET"])
def productos():
    return render_template("productos.html", products=product_data)


# Ruta de saludo
@app.route("/saludo", methods=["GET"])
def saludo():
    nombre = request.args.get("nombre", "Invitado")
    return render_template("saludo.html", nombre=nombre)


# Ruta de login
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "" or password == "":
            error = "Por favor, complete todos los campos."
        elif username != "admin" or password != "secret":
            error = "Usuario o contraseña incorrectos."
        else:
            session["username"] = username
            return redirect(url_for("bienvenida"))

    return render_template("login.html", error=error)


# Ruta de contacto
@app.route("/contacto", methods=["GET", "POST"])
def contacto():
    if request.method == "POST":
        # Aquí iría la lógica para procesar el formulario de contacto
        nombre = request.form.get("nombre")
        email = request.form.get("email")
        mensaje = request.form.get("mensaje")
        # Procesar los datos (no implementado)
        return render_template("confirmacion.html", nombre=nombre)
    return render_template("contacto.html")


@app.route("/bienvenida", methods=["GET"])
def bienvenida():
    if "username" in session:
        username = session["username"]
        return render_template("bienvenida.html", username=username)
    else:
        return redirect(url_for("login"))


@app.route("/logout", methods=["GET"])
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))


@app.route("/tema", methods=["GET"])
def tema():
    response = make_response(render_template("tema.html"))
    response.set_cookie(
        "modo", "oscuro", max_age=60 * 60 * 24 * 30
    )  # Cookie válida por 30 días
    return response


@app.route("/ver-tema", methods=["GET"])
def ver_tema():
    modo = request.cookies.get("modo")
    return f"El modo actual es: {modo}"


# Ejecutar la aplicación
if __name__ == "__main__":
    app.run(debug=True, port=5000)
