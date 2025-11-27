import joblib

# Carregar modelos
sentiment_model = joblib.load("modelos/sentiment_pipeline.joblib")
genre_model = joblib.load("modelos/genre_pipeline.joblib")
mlb = joblib.load("modelos/mlb_genres.joblib")

print("=== TESTE DO CLASSIFICADOR DE FILMES ===\n")

# Digite uma frase para testar
texto = input("Digite a descrição do filme: ")

# ---- SENTIMENTO ----
sentimento = sentiment_model.predict([texto])[0]

# ---- GÊNEROS ----
generos_bin = genre_model.predict([texto])
generos = mlb.inverse_transform(generos_bin)[0]

print("\nRESULTADO:")
print("---------------------------")
print(f"Sentimento detectado: {sentimento}")
print(f"Gêneros sugeridos: {', '.join(generos) if generos else 'Nenhum gênero detectado'}")
print("---------------------------")
