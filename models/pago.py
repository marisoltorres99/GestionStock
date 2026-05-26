from models.db import db
from datetime import datetime

class Pago(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    monto = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"), nullable=False)

    cliente = db.relationship("Cliente")

    cliente = db.relationship("Cliente", back_populates="pagos")