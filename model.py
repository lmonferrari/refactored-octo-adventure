import os
import pandas as pd
import joblib
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report

BASEDIR = os.path.abspath(os.path.dirname(__file__))
ARTIFACTS_DIR = os.path.join(BASEDIR, "artifacts")
engine = create_engine("sqlite:///" + os.path.join(BASEDIR, "db.sqlite3"), echo=True)

# recupera os dados do banco de dados
with engine.connect() as con:
    df_products = pd.read_sql_query("SELECT * FROM products", con)

# separa os dados em features e target
X = df_products.drop(columns=["id", "name"])
y = df_products["name"]

# cria os conjuntos de treino e teste
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=1,
)

# codifica as variáveis categóricas
le_packing = LabelEncoder()
le_packing.fit(X_train["packing"])

le_name = LabelEncoder()
le_name.fit(y_train)

# aplica a codificação nos conjuntos de treino e teste
X_train["packing"] = le_packing.transform(X_train["packing"])
X_test["packing"] = le_packing.transform(X_test["packing"])

y_train = le_name.transform(y_train)
y_test = le_name.transform(y_test)

# Treina o modelo
model = DecisionTreeClassifier(random_state=1)
model.fit(X_train, y_train)
predictions = model.predict(X_test)

# avalia o modelo
print("Accuracy:", accuracy_score(y_test, predictions))
print(classification_report(y_test, predictions))

# # salvando os objetos de codificação
joblib.dump(le_name, open(os.path.join(ARTIFACTS_DIR, "le_name.pkl"), "wb"))
joblib.dump(le_packing, open(os.path.join(ARTIFACTS_DIR, "le_packing.pkl"), "wb"))
joblib.dump(model, open(os.path.join(ARTIFACTS_DIR, "model.pkl"), "wb"))
