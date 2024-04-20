import os
from joblib import load
from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

BASEDIR = os.path.abspath(os.path.dirname(__file__))
DBPATH = os.path.join(BASEDIR, "db.sqlite3")
ARTIFACTSPATH = os.path.join(BASEDIR, "artifacts/")

model = load(ARTIFACTSPATH + "model.pkl")
le_name = load(ARTIFACTSPATH + "le_name.pkl")
le_packing = load(ARTIFACTSPATH + "le_packing.pkl")

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


@app.route("/predict", methods=["POST"])
def predict():
    packing = le_packing.transform([request.form.get("packing")])[0]
    weight = int(request.form.get("weight"))

    prediction = model.predict([[weight, packing]])[0]
    prediction = le_name.inverse_transform([prediction])[0]

    print(f"Prediction: {prediction}")

    return jsonify({"product": prediction})


if __name__ == "__main__":
    app.run(debug=True)
