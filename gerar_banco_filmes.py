import pandas as pd
import random
import os

# Lista de gêneros comuns
generos = [
    "Ação", "Aventura", "Comédia", "Drama", "Terror", "Ficção Científica",
    "Fantasia", "Romance", "Suspense", "Mistério", "Animação"
]

# Funções para gerar dados aleatórios
def gerar_titulo():
    palavras = ["A Lenda", "O Segredo", "A Jornada", "O Último", "A Nova Era",
                "O Retorno", "A Guerra", "O Portal", "A Missão", "O Reinado",
                "No Limite", "Além", "O Enigma", "A Chave", "O Fragmento"]
    complemento = ["do Tempo", "da Escuridão", "da Magia", "do Herói",
                   "da Morte", "das Sombras", "da Luz", "do Infinito",
                   "da Verdade", "do Amanhã"]
    return f"{random.choice(palavras)} {random.choice(complemento)}"

def gerar_sinopse():
    frases = [
        "Um herói improvável descobre um poder oculto.",
        "Uma força misteriosa ameaça o futuro da humanidade.",
        "Uma jornada épica começa quando um segredo antigo é revelado.",
        "Amigos precisam enfrentar seus maiores medos para sobreviver.",
        "Uma cidade isolada guarda mistérios sombrios.",
        "Um romance improvável nasce em meio ao caos.",
        "Um grupo precisa impedir uma catástrofe mundial.",
        "Uma criatura misteriosa surge mudando tudo.",
        "Um cientista faz uma descoberta que altera o destino humano.",
        "O protagonista enfrenta sua maior perda."
    ]
    return " ".join(random.choice(frases) for _ in range(3))

# Gera os filmes
filmes = []
for i in range(1000):
    filmes.append({
        "titulo": f"{gerar_titulo()} ({i+1})",
        "genero": random.choice(generos),
        "ano": random.randint(1980, 2025),
        "sinopse": gerar_sinopse(),
        "nota": round(random.uniform(1.0, 10.0), 1)
    })

# Cria DataFrame
df = pd.DataFrame(filmes)

# Cria pasta se não existir
os.makedirs("dados", exist_ok=True)

# Salva CSV
df.to_csv("dados/filmes.csv", index=False, encoding="utf-8")

print("✔ Base de 1000 filmes criada com sucesso em dados/filmes.csv")
