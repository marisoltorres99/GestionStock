from flask import Blueprint, render_template, request, redirect, url_for
from models.pago import Pago
from models.cliente import Cliente
from models.db import db

informe_bp = Blueprint("informe", __name__)

@informe_bp.route("/informes")
def listar():
    return render_template("informes/index.html")
