import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import accuracy_score, f1_score
from sklearn.multiclass import OneVsRestClassifier
import joblib
import os

# Criar pasta modelos se não existir
os.makedirs("modelos", exist_ok=True)

print("Carregando arquivos CSV...")

# === SENTIMENTO ===
reviews = pd.read_csv("dados/reviews.csv")

print("Treinando modelo de SENTIMENTO...")

sentiment_pipeline = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", LogisticRegression(max_iter=200))
])

X_train, X_test, y_train, y_test = train_test_split(
    reviews["review"], reviews["sentiment"], test_size=0.2, random_state=42
)

sentiment_pipeline.fit(X_train, y_train)

preds = sentiment_pipeline.predict(X_test)
print("Acurácia Sentimento:", accuracy_score(y_test, preds))

# Salvar modelo
joblib.dump(sentiment_pipeline, "modelos/sentiment_pipeline.joblib")


# === GENEROS ===
print("Treinando modelo de GÊNEROS...")

movies = pd.read_csv("dados/movies.csv")
movies["genres"] = movies["genres"].apply(lambda x: x.split("|"))

mlb = MultiLabelBinarizer()
Y = mlb.fit_transform(movies["genres"])

genre_pipeline = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", OneVsRestClassifier(LogisticRegression(max_iter=300)))
])

X_train_g, X_test_g, y_train_g, y_test_g = train_test_split(
    movies["overview"], Y, test_size=0.2, random_state=42
)

genre_pipeline.fit(X_train_g, y_train_g)

y_pred_g = genre_pipeline.predict(X_test_g)

print("Micro-F1:", f1_score(y_test_g, y_pred_g, average="micro"))
print("Macro-F1:", f1_score(y_test_g, y_pred_g, average="macro"))

# Salvar modelos
joblib.dump(genre_pipeline, "modelos/genre_pipeline.joblib")
joblib.dump(mlb, "modelos/mlb_genres.joblib")

print("\nModelos treinados e salvos com sucesso!")
