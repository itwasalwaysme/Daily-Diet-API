from models.items import Item
from flask import Flask, jsonify, request
from database import db
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = "key"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root@localhost:3306/diet-api"

db.init_app(app)

@app.route("/item", methods=['POST'])
def add_item():
    data = request.get_json()
    item = data.get("item")
    desc = data.get("descricao")
    dentro_da_dieta = data.get("dentro_da_dieta")

    if item:
        data = datetime.now().strftime("%d/%m/%Y %H:%M")
        item = Item(item=item, descricao=desc, data_hora=data, dentro_da_dieta=dentro_da_dieta)
        db.session.add(item)
        db.session.commit()
        return jsonify({"message": "Item adicionado a lista"}), 200
    
    return jsonify({"message": "Dados inválidos"}), 400

@app.route("/item/<int:id>", methods=['PUT'])
def edit_item(id):
    data = request.get_json()
    item_name = data.get("item")
    desc = data.get("descricao")
    data_hora = data.get("data_hora")
    dentro_da_dieta = data.get("dentro_da_dieta")
    
    if item_name and dentro_da_dieta:
        item = Item.query.get(id)
        if item:
            item.item = item_name
            item.descricao = desc
            item.data_hora = data_hora
            item.dentro_da_dieta = dentro_da_dieta
            db.session.commit()
            return jsonify({"message": "Items atualizados"}), 200
        else:
            return jsonify({"message": "Item inválido"}), 404

    return jsonify({"message": "Dados inválidos"}), 400

@app.route("/item/<int:id>", methods=['DELETE'])
def remove_item(id):
    item = Item.query.get(id)

    if item:
        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": "Item excluido"}), 200
    
    return jsonify({"message": "Item inválido"}), 404

@app.route("/items", methods=['POST'])
def view_all_items():
    items = Item.query.all()
    result = []
    if items:
        for item in items:
            result.append({
                "item_name": item.item,
                "descricao": item.descricao,
                "data_hora": item.data_hora,
                "dentro_da_dieta": item.dentro_da_dieta
            })
        return jsonify({"items": result}), 200

    return jsonify({"message": "Nenhum item encontrado"}), 404

@app.route("/item/<int:id>", methods=['GET'])
def view_item(id):
    item = Item.query.get(id)

    if item:
        return jsonify({"item": {
            "item_name": item.item,
            "descricao": item.descricao,
            "data_hora": item.data_hora,
            "dentro_da_dieta": item.dentro_da_dieta,
        }}), 200

    return jsonify({"message": "Dados inválidos"}), 404

if __name__ == "__main__":
    app.run(debug=True)