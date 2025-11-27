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
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

# Create a Flask application instance
app = Flask(__name__)
app.secret_key = "clave_super_secreta"  # Necesaria para manejar sesiones
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Modelos de ejemplo
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    edad = db.Column(db.Integer, nullable=True)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<Usuario {self.nombre}>"


# Crear la base de datos
with app.app_context():
    db.create_all()


# Ruta de registro
@app.route("/registro", methods=["GET", "POST"])
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
            return redirect(url_for("login"))

    return render_template("registro.html", error=error)


# Ruta de login
@app.route("/login", methods=["GET", "POST"])
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
                return redirect(url_for("panel"))
            else:
                error = "Credenciales inválidas. Intente de nuevo."

    return render_template("login.html", error=error)


# Ruta de panel
@app.route("/panel", methods=["GET"])
def panel():
    if "usuario_id" in session:
        usuario_nombre = session["usuario_nombre"]
        return render_template("panel.html", usuario_nombre=usuario_nombre)
    else:
        return redirect(url_for("login"))


@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for("login"))


# Ruta principal
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


# CRUD - CREATE, READ, UPDATE, DELETE


@app.route("/usuarios", methods=["GET", "POST"])
def usuarios():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        email = request.form.get("email")
        # INSERT nuevo usuario en la base de datos
        nuevo_usuario = Usuario(nombre=nombre, email=email)
        db.session.add(nuevo_usuario)
        db.session.commit()
        return redirect(url_for("usuarios"))

    # SELECT * FROM usuarios
    usuarios = Usuario.query.all()
    return render_template("usuarios.html", usuarios=usuarios)


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    usuario = Usuario.query.get_or_404(id)

    if request.method == "POST":
        usuario.nombre = request.form.get("nombre")
        usuario.email = request.form.get("email")
        db.session.commit()
        return redirect(url_for("usuarios"))
    return render_template("editar_usuario.html", usuario=usuario)


@app.route("/eliminar/<int:id>")
def eliminar(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for("usuarios"))


@app.route("/buscar/<int:id>", methods=["GET"])
def buscar(id):
    usuario = Usuario.query.get_or_404(id)
    return f"Usuario encontrado: {usuario.nombre} ({usuario.email})"


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
