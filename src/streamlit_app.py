import streamlit as st
import os
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

# ================================
# CARREGAR VARIÁVEIS DE AMBIENTE
# ================================
load_dotenv()

# Inicializa o cliente sem passar API Key manualmente
client = OpenAI()

# ================================
# CONFIGURAÇÃO DO STREAMLIT
# ================================
st.set_page_config(page_title="Classificador de Filmes", page_icon="🎬", layout="centered")

st.title("🎬 Classificador de Filmes")
st.write("Digite a sinopse de um filme e receba uma classificação automática e recomendações!")

# ================================
# CARREGAR BANCO DE FILMES
# ================================
try:
    df = pd.read_csv("dados/filmes.csv")
except Exception as e:
    st.error("❌ Erro ao carregar dados/filmes.csv. Verifique se o arquivo existe.")
    st.stop()

# ================================
# CAIXA DE TEXTO
# ================================
sinopse = st.text_area("Insira a sinopse do filme:", height=250)

# ================================
# BOTÃO DE CLASSIFICAR
# ================================
if st.button("Classificar"):
    if not sinopse.strip():
        st.warning("Por favor, insira uma sinopse antes de classificar.")
    else:

        with st.spinner("Classificando..."):

            # Chamada correta para modelos OpenAI (2024+)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Você é um classificador de filmes. "
                            "Dado uma sinopse, retorne apenas o gênero principal do filme, "
                            "como: Ação, Romance, Drama, Terror, Ficção Científica, Animação, Crime, etc."
                        )
                    },
                    {
                        "role": "user",
                        "content": sinopse
                    }
                ],
                max_tokens=50
            )

            # Extrair texto corretamente
            classificacao = response.choices[0].message.content

        # Exibe resultado da IA
        st.success("Classificação concluída!")
        st.subheader("🎯 Gênero identificado pela IA:")
        st.write(f"**{classificacao}**")

        # ================================
        # RECOMENDAÇÕES DO BANCO LOCAL
        # ================================
        st.subheader("📚 Recomendações do Banco de Dados:")

        genero = classificacao.split()[0]  # pega a primeira palavra do gênero

        # procura filmes cujo gênero contenha essa palavra
        resultados = df[df["genero"].str.contains(genero, case=False, na=False)]

        if resultados.empty:
            st.write("Nenhum filme encontrado na base para este gênero.")
        else:
            st.write(f"Filmes do gênero relacionado a **{genero}** encontrados:")

            # mostra no máximo 5 aleatórios
            for _, row in resultados.sample(min(5, len(resultados))).iterrows():
                st.markdown(
                    f"""
                    **🎬 {row['titulo']} ({row['ano']})**  
                    ⭐ Nota: {row['nota']}  
                    📌 *{row['sinopse']}*  
                    ---
                    """
                )
