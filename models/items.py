from database import db
from flask_login import UserMixin

class Item(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255), nullable=True)
    data_hora = db.Column(db.String(50), nullable=False)
    dentro_da_dieta = db.Column(db.String(40), nullable=False)