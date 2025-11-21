from flask import Flask, render_template, request

# Create a Flask application instance
app = Flask(__name__)

# Sample user data
user_data = {
    "nombre": "Francisco Suárez",
    "edad": 26,
    "correo": "francisco.suarez@example.com",
}

# Sample product data
product_data = [
    {"nombre": "Producto A", "precio": 100},
    {"nombre": "Producto B", "precio": 200},
    {"nombre": "Producto C", "precio": 300},
]


# Ruta principal
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


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
    if request.method == "POST":
        # Aquí iría la lógica para procesar el login
        username = request.form.get("username")
        password = request.form.get("password")
        # Validar credenciales (no implementado)
        return render_template("bienvenida.html", username=username)
    return render_template("login.html")


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


# Ejecutar la aplicación
if __name__ == "__main__":
    app.run(debug=True, port=5000)
