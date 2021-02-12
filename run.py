from flask import Flask, jsonify, g, abort, request
import sqlite3

app = Flask(__name__)
DATABASE = "app.db"


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.route("/categories", methods=["GET"])
def index_categories():
    try:
        if request.method == "GET":
            categories = []
            for cat in cursor:
                categories.append({"id": cat[0], "name": cat[1]})
            return jsonify(categories)
    except IndexError:
        abort(404)
    except NameError:
        abort(404)


@app.route("/categories", methods=["POST"])
def insert_categories():
    try:
        if request.method == "POST":
            entrée = request.values.get("name")
            db = get_db()
            cursor = db.execute(
                "INSERT INTO categories (name) values (?)", [entrée])
            db.commit()
            cursor = db.execute(
                "SELECT id, name FROM categories WHERE name = (?)", [entrée])
            sortie = cursor.fetchone()
            return jsonify({"id": sortie[0], "name": sortie[1]})
    except IndexError:
        abort(404)
    except NameError:
        abort(404)


@app.route("/categories/<cat_id>", methods=["PUT"])
def update_categories(cat_id):
    try:
        if request.method == "PUT":
            entrée = request.values.get("name")
            db = get_db()
            cursor = db.execute(
                "UPDATE categories SET name = (?)  WHERE id= (?)", (entrée, cat_id))
            db.commit()
            cursor = db.execute(
                "SELECT id, name FROM categories WHERE  id = (?)", [cat_id])
            sortie = cursor.fetchone()
            return jsonify({"id": sortie[0], "name": sortie[1]})
    except IndexError:
        abort(404)
    except NameError:
        abort(404)


@app.route("/categories/<cat_id>", methods=["DELETE"])
def destroy_categories(cat_id):
    try:
        if request.method == "DELETE":
            db = get_db()
            sortie = db.execute(
                "SELECT id, name FROM categories WHERE  id = (?)", [cat_id])
            cursor = db.execute(
                "DELETE FROM categories WHERE id= (?)", (cat_id))
            william = sortie.fetchone()
            db.commit()
            db.close()
            return jsonify({"id": william[0], "name": william[1]})
    except IndexError:
        abort(404)
    except NameError:
        abort(404)


@app.route("/categories/<cat_id>", methods=["GET", "POST"])
def show_categories(cat_id):
    if request.method == "GET":
        db = get_db()
        cursor = db.execute(
            "SELECT id, name FROM categories WHERE id = ?", [cat_id])
        category = cursor.fetchone()
        if category == None:
            abort(404)
        return jsonify({"id": category[0], "name": category[1]})


if __name__ == "__main__":
    app.run(debug=True)
