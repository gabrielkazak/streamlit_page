import streamlit as st
from utils.carrega_dados import carregar_dados

df=carregar_dados()

st.set_page_config(
  page_title="BackLoggd",
  page_icon="🎮",
)


st.title('🎮 BackLoggd')

st.markdown(f"""
Bem-vindo ao **BackLoggd**!

Este aplicativo interativo foi desenvolvido para explorar e visualizar as principais informações de um conjunto de dados sobre **jogos digitais**, abrangendo o período de **1980 a 2023** — praticamente toda a história dos videogames modernos. 🕹️

Ao navegar pelas páginas no menu lateral (sidebar), você poderá explorar diversas análises feitas com base nesses dados. A ideia é entender como os jogos evoluíram ao longo do tempo e como impactaram o público gamer mundialmente.

---

### 🔍 Perguntas que buscamos responder:

- **Quais desenvolvedoras publicaram mais jogos?**
- **Qual foi o período com mais lançamentos?**
- **Quais são os gêneros mais populares ao longo dos anos?**

---
   
### 📐 Dimensões do conjunto de dados:
- **Linhas:** `{df.shape[0]}`
- **Colunas:** `{df.shape[1]}`

---
""")

st.header("Visão Geral dos Dados Principais")
st.dataframe(df.head())

st.markdown(
    """
#### Site desenvolvido como requisito final para **Programação III**.
##### Desenvolvido por: Arthur dos Reis e Gabriel da Silva Kazakevicius
"""
)


