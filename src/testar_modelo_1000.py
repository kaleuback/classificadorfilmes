import pandas as pd
from openai import OpenAI
import random
import os
from dotenv import load_dotenv

# Carrega API KEY
load_dotenv()
client = OpenAI()

# Carrega o banco de 1000 filmes
df = pd.read_csv("dados/filmes.csv")

print("📚 Total de filmes carregados:", len(df))
print("="*80)

# Escolhe quantos filmes você quer testar
NUM_TESTES = 15  # altere para 100 se quiser testar 100, etc.

amostras = df.sample(NUM_TESTES)

for index, row in amostras.iterrows():
    titulo = row["titulo"]
    sinopse = row["sinopse"]
    genero_real = row["genero"]

    print(f"\n🎬 Testando filme: {titulo}")
    print(f"🎭 Gênero REAL: {genero_real}")

    # Chama o modelo
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Você é um classificador de filmes. Seu trabalho é identificar o gênero com base na sinopse."
            },
            {"role": "user", "content": sinopse}
        ],
        max_tokens=150
    )

    genero_previsto = response.choices[0].message.content

    print("🤖 Gênero PREVISTO pelo modelo:", genero_previsto)
    print("-" * 80)

print("\n✔ Testes concluídos!")
