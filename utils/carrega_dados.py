import pandas as pd
import streamlit as st
import plotly.express as px

@st.cache_data
def carregar_dados():
    df_original = pd.read_csv('./dataset/backloggd_games_fixed.csv')
    return df_original

def ensure_list(x):
    if isinstance(x, list):
        return x
    elif isinstance(x, str):
        return x.replace('[','').replace(']','').replace("'", "").split(', ')
    else:
        return []
    
def load_images():
    jogos = [
        {"nome": "Minecraft", "imagem": "images/minecraft.png"},
        {"nome": "The Legend of Zelda: BOTW", "imagem": "images/zelda.png"},
        {"nome": "GTA V", "imagem": "images/gtav.png"},
        {"nome": "Portal 2", "imagem": "images/portal2.png"},
        {"nome": "Undertale", "imagem": "images/undertale.png"},
    ]

    cols = st.columns(5)

    for idx, col in enumerate(cols):
        with col:
            st.image(jogos[idx]["imagem"], use_container_width=True)
            st.markdown(f"<center><b>{jogos[idx]['nome']}</b></center>", unsafe_allow_html=True)
        
def return_devs():
    # Dados originais
    dados = {
        "Japão": 24,
        "Estados Unidos": 26,
        "França": 4,
        "Canadá": 2,
        "Reino Unido": 6,
        "Hong Kong": 2,
        "Suécia": 1,
        "Áustria": 1,
        "Itália": 1,
        "Polônia": 1,
        "Alemanha": 1
    }
    paises_europa = ["França", "Reino Unido", "Suécia", "Áustria", "Itália", "Polônia", "Alemanha"]
    total_europa = sum(dados[pais] for pais in paises_europa)

    for pais in paises_europa:
        dados.pop(pais)

    dados["Europa"] = total_europa

    df = pd.DataFrame({
        "País": list(dados.keys()),
        "Quantidade": list(dados.values())
    })

    dark_colors = ["#390000", "#7D7F03", '#3d2c8d', "#007c11", '#4a4e69', '#22223b', '#0f3460', '#53354a']

    fig = px.pie(
        df, 
        names='País', 
        values='Quantidade', 
        hole=0.5, 
        color_discrete_sequence=dark_colors
    )

    return fig