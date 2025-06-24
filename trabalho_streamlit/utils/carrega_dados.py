import pandas as pd;
import streamlit as st
import requests

@st.cache_data
def carregar_dados():
    df_original = pd.read.csv('../dataset/backloggd_games_fixed.csv')

    