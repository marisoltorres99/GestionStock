from models.db import db
from datetime import datetime

class Venta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Float, nullable=False)

    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"), nullable=True)

    detalles = db.relationship("DetalleVenta", backref="venta", lazy=True)