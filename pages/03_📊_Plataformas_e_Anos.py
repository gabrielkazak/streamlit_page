import streamlit as st
from utils.carrega_dados import carregar_dados, ensure_list
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(
  page_title="BackLoggd",
  page_icon="🎮",
)

df = carregar_dados()

st.title("🎮 BackLoggd")
st.title("Análise de Plataformas e Cronologia dos Jogos")

st.markdown("### 🎮 Distribuição de Jogos por Plataforma")

df_platforms = df[df['Platforms'].notnull()].copy()
df_platforms['Platforms'] = df_platforms['Platforms'].apply(ensure_list)
df_platforms = df_platforms.explode('Platforms')
platform_counts = df_platforms['Platforms'].value_counts().reset_index()
platform_counts.columns = ['Plataforma', 'Quantidade']

with st.expander("Personalizar Plataformas (Filtrar)", expanded=False):
    min_jogos = st.slider("Quantidade mínima de jogos:", 
                         min_value=int(platform_counts['Quantidade'].min()),
                         max_value=int(platform_counts['Quantidade'].max()),
                         value=int(platform_counts['Quantidade'].max()/10))
    
    tipos_plat = st.multiselect(
        "Escolha os tipos de plataforma para visualizar:",
        options=["PC", "PlayStation", "Xbox", "Nintendo", "Mobile", "Outros"],
        default=["PC", "PlayStation", "Xbox", "Nintendo"]
    )

def categorizar_plataforma(plataforma):
    plataforma = plataforma.lower()
    if "windows" in plataforma or "pc" in plataforma or "mac" in plataforma or "linux" in plataforma:
        return "PC"
    elif "playstation" in plataforma:
        return "PlayStation"
    elif "xbox" in plataforma:
        return "Xbox"
    elif "nintendo" in plataforma or "wii" in plataforma or "switch" in plataforma:
        return "Nintendo"
    elif "android" in plataforma or "ios" in plataforma:
        return "Mobile"
    else:
        return "Outros"

platform_counts['Categoria'] = platform_counts['Plataforma'].apply(categorizar_plataforma)

filtered_platforms = platform_counts[
    (platform_counts['Quantidade'] >= min_jogos) & 
    (platform_counts['Categoria'].isin(tipos_plat))
]

filtered_platforms = filtered_platforms.sort_values('Quantidade', ascending=False)

fig = px.bar(
    filtered_platforms,
    x='Plataforma',
    y='Quantidade',
    color='Categoria',
    labels={'Plataforma': 'Plataforma', 'Quantidade': 'Número de Jogos'},
    height=500
)

fig.update_layout(
    xaxis_tickangle=-45,
    xaxis={'categoryorder':'total descending'}
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
    O gráfico de barras acima mostra a distribuição de jogos por plataforma no conjunto de dados.
    É possível observar que algumas plataformas como PC e consoles da geração atual dominam o mercado,
    com uma grande variedade de títulos disponíveis em múltiplos sistemas.
    
    A possibilidade de filtrar por categoria e quantidade mínima permite analisar diferentes segmentos do mercado
    e entender a popularidade relativa entre consoles, PC e dispositivos móveis ao longo dos anos.
    
    Algumas plataformas mais antigas ou menos populares têm menor representação, mas ainda assim
    contribuem para a diversidade do ecossistema de jogos.
""")

st.markdown("### 📅 Evolução do Lançamento de Jogos por Ano")

df_anos = df.copy()
df_anos['release_year'] = pd.to_datetime(df_anos['Release_Date'], errors='coerce').dt.year
jogos_por_ano = df_anos['release_year'].value_counts().sort_index()
jogos_por_ano = jogos_por_ano[jogos_por_ano.index >= 1980] # Filtrando anos anteriores a 1980

fig2 = go.Figure()

fig2.add_trace(go.Scatter(
    x=jogos_por_ano.index,
    y=jogos_por_ano.values,
    mode='lines',
    name='Quantidade de Jogos',
    fill='tozeroy',
    line=dict(color='rgba(76, 175, 80, 0.8)', width=3)
))

eventos = {
    1985: "NES",
    1994: "PlayStation",
    2001: "Xbox",
    2006: "Wii",
    2013: "PS4/Xbox One",
    2017: "Switch",
    2020: "PS5/Xbox Series"
}

for ano, evento in eventos.items():
    if ano in jogos_por_ano.index:
        fig2.add_annotation(
            x=ano,
            y=jogos_por_ano[ano],
            text=evento,
            showarrow=True,
            arrowhead=1
        )

fig2.update_layout(
    title="Evolução de Lançamentos de Jogos (1980-2023)",
    xaxis_title="Ano",
    yaxis_title="Quantidade de Jogos",
    height=500
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("""
    O gráfico acima mostra a evolução da quantidade de jogos lançados por ano desde 1980.
    Podemos observar claramente o crescimento da indústria ao longo das décadas, com picos significativos
    que geralmente coincidem com o lançamento de novas gerações de consoles.
    
    Alguns pontos de destaque incluem:
    - O boom inicial dos jogos na era do NES (1985-1990)
    - A explosão de títulos com a chegada do PlayStation (1995-2000)
    - O crescimento constante durante a era do PS2/Xbox/GameCube
    - A diversificação e expansão massiva durante a década de 2010
    - A decadência de jogos por conta da pandemia

    Esta visualização nos permite entender como a indústria evoluiu e se adaptou ao longo do tempo,
    respondendo a mudanças tecnológicas e demandas do mercado.
""")

st.markdown("### 🎲 Relação entre Jogos Mais Jogados vs. Jogados Atualmente")

top_games = df.nlargest(10, 'Plays').copy()
top_games = top_games[['Title', 'Plays', 'Playing', 'Rating']]
top_games['Razão Playing/Plays'] = (top_games['Playing'] / top_games['Plays'] * 100).round(2)
top_games = top_games.sort_values('Razão Playing/Plays', ascending=False)

fig3 = px.scatter(
    top_games,
    x='Plays',
    y='Playing',
    size='Rating',
    color='Razão Playing/Plays',
    hover_name='Title',
    size_max=50,
    color_continuous_scale='Viridis',
    labels={
        'Plays': 'Total de Jogadores',
        'Playing': 'Jogadores Atualmente',
        'Rating': 'Avaliação'
    },
    height=600
)

fig3.update_layout(
    coloraxis_colorbar=dict(
        title='% Playing/Plays'
    )
)

for i, row in top_games.iterrows():
    fig3.add_annotation(
        x=row['Plays'],
        y=row['Playing'],
        text=row['Title'],
        showarrow=True,
        arrowhead=1,
        ax=0,
        ay=-30
    )

st.plotly_chart(fig3, use_container_width=True)

st.markdown("""
    Este gráfico de dispersão apresenta uma análise interessante sobre os jogos mais populares,
    comparando o número total de pessoas que já jogaram (Plays) com aquelas que estão jogando
    ativamente no momento (Playing).
    
    O tamanho de cada bolha representa a avaliação média do jogo, enquanto a cor indica a 
    proporção entre jogadores ativos e o total de jogadores que já experimentaram o título.
    
    Jogos com altos valores tanto em "Plays" quanto em "Playing" são verdadeiros clássicos
    que mantêm sua relevância ao longo do tempo, enquanto títulos com alto "Playing" em
    relação ao "Plays" indicam lançamentos mais recentes ou jogos com forte retenção de jogadores.
    
    Esta visualização nos ajuda a identificar quais jogos têm maior longevidade e quais
    conseguem manter sua base de jogadores engajada por mais tempo.
""")