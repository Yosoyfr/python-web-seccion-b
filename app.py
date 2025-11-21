from flask import Flask, render_template

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
@app.route("/")
def home():
    return render_template("index.html")


# Ruta de perfil
@app.route("/perfil")
def perfil():
    return render_template("perfil.html", user=user_data)


# Ruta de productos
@app.route("/productos")
def productos():
    return render_template("productos.html", products=product_data)


# Ruta de contacto
@app.route("/contacto")
def contacto():
    return render_template("contacto.html")


# Ejecutar la aplicación
if __name__ == "__main__":
    app.run(debug=True, port=5000)
