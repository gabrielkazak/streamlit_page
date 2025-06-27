import streamlit as st
from utils.carrega_dados import carregar_dados, ensure_list, load_images, return_devs
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd



st.set_page_config(
  page_title="BackLoggd",
  page_icon="🎮",
)

df = carregar_dados()

st.title("🎮 BackLoggd")

st.title("Gráficos Relacionados a Jogos mais jogados, Gênero e Desenvolvedoras")






st.markdown("### 🧩 Distribuição de jogos por gênero")

df_genres = df[df['Genres'].notnull()].copy()

df_genres['Genres'] = df_genres['Genres'].apply(ensure_list)

df_genres = df_genres.explode('Genres')

genre_counts = df_genres['Genres'].value_counts()

generos_disponiveis = genre_counts.index.tolist()

generos_remover = []

with st.expander("Personalizar Gêneros (Remover do gráfico)", expanded=False):
    generos_remover = st.multiselect(
        "Escolha os gêneros que deseja remover:",
        options=generos_disponiveis,
        default=[]
    )

generos_para_mostrar = [g for g in generos_disponiveis if g not in generos_remover]

genre_counts_filtrado = genre_counts[genre_counts.index.isin(generos_para_mostrar)]

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=genre_counts_filtrado.index,
    y=genre_counts_filtrado.values,
    mode='lines+markers',
    fill='tozeroy',
    name='Quantidade de jogos'
))

fig.update_layout(
    xaxis_title='Gênero',
    yaxis_title='Quantidade de jogos',
    xaxis_tickangle=-90,
    height=500
)
st.plotly_chart(fig, use_container_width=True)

st.markdown(
    "O gráfico de linhas mostra a distribuição de jogos por gênero, revelando tendências marcantes dentro do mercado de games. "
    "O gênero **Aventura** aparece como o mais recorrente, englobando uma grande variedade de títulos que priorizam exploração e narrativa. "
    "Logo em seguida, o destaque vai para os jogos **Indie**, o que evidencia o crescimento e a relevância dos desenvolvedores independentes, "
    "que têm conquistado espaço com produções criativas e inovadoras, muitas vezes com orçamentos reduzidos. "
    "Outros gêneros como **RPG**, **Shooter** e **Plataforma** também aparecem com grande representatividade, "
    "refletindo a diversidade de estilos que compõem a indústria e a variedade de preferências entre os jogadores."
)






st.markdown("### ⌚ Top 5 Jogos mais jogados historicamente e atualmente")

top_plays_playing = df.sort_values(['Plays', 'Playing'], ascending=False).head(5)
df_melted = top_plays_playing.melt(id_vars='Title', value_vars=['Plays', 'Playing'],var_name='Tipo', value_name='Quantidade')
fig = px.bar(df_melted, 
             x='Quantidade', 
             y='Title', 
             color='Tipo', 
             orientation='h',
             labels={'Quantidade':'Quantidade', 'Title':'Jogo', 'Tipo':'Métrica'},
             height=500)
fig.update_layout(yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig, use_container_width=True)

load_images()

st.markdown(
    "O gráfico de barras empilhadas exibe os cinco jogos mais jogados da história e dos dias atuais de acordo com as métricas obtidas pelo criador do conjunto de dados, "
    "permitindo uma comparação visual entre a popularidade acumulada e a relevância contínua de cada título. "
    "O destaque fica para **Minecraft (2009)**, que lidera a o conjunto de dados, evidenciando seu impacto duradouro na cultura gamer. "
    "**The Legend of Zelda: Breath of the Wild**, **GTA V**, **Portal 2** e **Undertale** completam o ranking, "
    "representando diferentes gêneros e estilos de jogo que marcaram gerações e mantêm comunidades ativas ao longo do tempo."
)





st.markdown("### 📈 Empresas Desenvolvedoras com mais jogos publicados")


df_devs = df[df['Developers'] != '[]'].copy()
df_devs['Developers'] = df_devs['Developers'].str.strip("[]").str.replace("'", "")
top_developers = df_devs['Developers'].value_counts().head(9)
top_developers_df = top_developers.reset_index()
top_developers_df.columns = ['Developer', 'Quantidade']
fig = px.bar(top_developers_df, 
             x='Developer', 
             y='Quantidade', 
             labels={'Developer': 'Developer', 'Quantidade': 'Quantidade de jogos'},
             height=500)
fig.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig, use_container_width=True)

st.markdown(
    "O gráfico de barras apresenta as nove desenvolvedoras com maior número de jogos publicados no conjunto de dados, "
    "lideradas pela **Capcom**, seguida por nomes como **Konami**, **Nintendo** e **Square Enix**. "
    "Nota-se que a maioria dessas empresas são **japonesas**, o que reflete a longa tradição e influência do Japão no cenário global de videogames. "
    "Esse domínio pode ser atribuído ao fato de o país possuir um dos mercados mais antigos e consolidados da indústria, "
    "sendo berço de franquias icônicas e responsável por moldar grande parte da cultura gamer moderna. "
    "Empresas como **Telltale Games**, **Gameloft** e **Activision** também figuram no ranking, mostrando a diversidade geográfica, "
    "ainda que o protagonismo japonês seja evidente."
)





st.markdown("### 🌎 Gráfico auxiliar mostrando a divisão do mercado de Desenvolvedoras com mais jogos publicados")

st.markdown("""
ℹ️ Os dados apresentados a seguir consideram apenas desenvolvedores com **pelo menos 50 jogos publicados**.

🌍 A **Europa** foi agrupada como uma única região para fins de visualização.
""")


st.plotly_chart(return_devs(), use_container_width=True)

st.markdown(
    "O gráfico de pizza acima ajuda a visualizar a distribuição do desenvolvimento de jogos por país. "
    "Foram considerados apenas desenvolvedores com pelo menos 50 jogos publicados, garantindo que as empresas mais tradicionais estejam representadas. "
    "Os Estados Unidos aparecem em primeiro lugar, principalmente devido à produção em massa que ocorreu a partir das décadas de 1980 e 1990. "
    "O Japão vem em segundo, refletindo sua indústria de videogames tradicional e influente ao longo dos anos."
)
