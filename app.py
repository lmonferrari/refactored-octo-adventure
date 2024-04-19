import os
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

BASEDIR = os.path.abspath(os.path.dirname(__file__))
DBPATH = os.path.join(BASEDIR, "db.sqlite3")

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + DBPATH
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Products(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    weight = db.Column(db.Float)
    packing = db.Column(db.String(50))

    def __repr__(self) -> str:
        return f"{self.name} - {self.weight} - {self.packing}"


@app.route("/", methods=["GET"])
def home():
    packing_types = Products.query.with_entities(Products.packing).distinct()
    packing_types = {packing.packing for packing in packing_types}

    return render_template("index.html", packing_types=packing_types)


if __name__ == "__main__":
    app.run(debug=True)
