from . import db
from datetime import datetime


# Modelo de Usuario para la autenticación
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    edad = db.Column(db.Integer, nullable=True)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, server_default=datetime.utcnow)

    productos = db.relationship("Producto", backref="creador", lazy=True)

    def __repr__(self):
        return f"<Usuario {self.nombre}>"


# Modelo de Productos
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(300), nullable=True)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, server_default=datetime.utcnow)

    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)

    def __repr__(self):
        return f"<Producto {self.nombre} - ${self.precio}>"
