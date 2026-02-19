import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Stock Dashboard", layout="wide")

st.title("📊 GOOGL Stock Dashboard")

# Caminho do CSV
file_path = Path(__file__).parent / "dados_tratados.csv"
df = pd.read_csv(file_path)

# Garantir datetime e ordenação
df['data'] = pd.to_datetime(df['data'])
df = df.sort_values('data')

# Criar colunas auxiliares
if 'Year' not in df.columns:
    df['Year'] = df['data'].dt.year
if 'Up' not in df.columns:
    df['Up'] = df['Fechamento'] > df['Abertura']

# --- Sidebar ---
st.sidebar.header("Filtros")

# Filtro de ano
ano = st.sidebar.selectbox("Selecione o Ano", sorted(df["Year"].unique()))

# Filtro de datas
data_inicio = st.sidebar.date_input("Data Início", df['data'].min())
data_fim = st.sidebar.date_input("Data Fim", df['data'].max())

# Filtro de dias da semana
dias_semana = st.sidebar.multiselect(
    "Selecione Dias da Semana",
    df['Dia_da_Semana'].unique(),
    default=list(df['Dia_da_Semana'].unique())
)

# Filtro de tipo de gráfico
grafico = st.sidebar.selectbox(
    "Escolha o gráfico",
    [
        "Fechamento x Abertura",
        "Subiu x Caiu (Pizza)",
        "Proporção por Dia da Semana (Pizza)",
        "Número de dias que subiu por Dia da Semana (Barra)",
        "Retorno Diário (%)",
        "Volume Diário"
    ]
)

# Aplicar filtros
df_filtrado = df[
    (df['Year'] == ano) &
    (df['data'] >= pd.to_datetime(data_inicio)) &
    (df['data'] <= pd.to_datetime(data_fim)) &
    (df['Dia_da_Semana'].isin(dias_semana))
]

# --- Gráficos ---
if grafico == "Fechamento x Abertura":
    st.subheader("Preço de Fechamento da Ação GOOGL")
    fig, ax = plt.subplots(figsize=(12,6))
    ax.plot(df_filtrado['data'], df_filtrado['Fechamento'], label='Fechamento', color='blue')
    ax.plot(df_filtrado['data'], df_filtrado['Abertura'], label='Abertura', color='orange')
    ax.set_title("Preço de Abertura x Fechamento")
    ax.set_xlabel("Data")
    ax.set_ylabel("Preço")
    ax.legend()
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

elif grafico == "Subiu x Caiu (Pizza)":
    st.subheader("Dias que Subiu x Caiu")
    contagem = df_filtrado["Up"].value_counts()
    fig2, ax2 = plt.subplots(figsize=(6,6))
    ax2.pie(
        contagem,
        labels=["Subiu", "Caiu"],
        autopct="%1.1f%%",
        startangle=90,
        colors=["#4CAF50", "#F44336"],
        textprops={'fontsize':12}
    )
    ax2.set_title("Proporção de dias que a ação subiu x caiu", fontsize=14)
    ax2.axis('equal')
    st.pyplot(fig2)

elif grafico == "Proporção por Dia da Semana (Pizza)":
    st.subheader("Proporção de dias que a ação subiu por dia da semana")
    dias_subiu = df_filtrado.groupby('Dia_da_Semana')['Up'].sum()
    fig3, ax3 = plt.subplots(figsize=(7,7))
    ax3.pie(dias_subiu, labels=dias_subiu.index, autopct='%1.1f%%', startangle=90)
    ax3.set_title("Proporção de dias que a ação subiu por dia da semana")
    st.pyplot(fig3)

elif grafico == "Número de dias que subiu por Dia da Semana (Barra)":
    st.subheader("Número de dias que a ação subiu por dia da semana")
    dias = df_filtrado.groupby('Dia_da_Semana')['Up'].sum()
    fig4, ax4 = plt.subplots(figsize=(8,5))
    dias.plot(kind='bar', color='skyblue', ax=ax4)
    ax4.set_title("Número de dias que a ação subiu por dia da semana")
    ax4.set_xlabel("Dia da Semana")
    ax4.set_ylabel("Quantidade de Dias")
    st.pyplot(fig4)

elif grafico == "Retorno Diário (%)":
    st.subheader("Retorno Diário (%) da ação GOOGL")
    fig5, ax5 = plt.subplots(figsize=(12,6))
    ax5.plot(df_filtrado['data'], df_filtrado['Retorno_Diário_Pct'], color='purple')
    ax5.set_title('Retorno Diário (%) GOOGL')
    ax5.set_xlabel('Data')
    ax5.set_ylabel('Retorno (%)')
    ax5.tick_params(axis='x', rotation=45)
    st.pyplot(fig5)

elif grafico == "Volume Diário":
    st.subheader("Volume diário de negociações GOOGL")
    fig6, ax6 = plt.subplots(figsize=(12,6))
    ax6.bar(df_filtrado['data'], df_filtrado['Volume'], color='orange')
    ax6.set_title('Volume diário de negociações GOOGL')
    ax6.set_xlabel('Data')
    ax6.set_ylabel('Volume')
    ax6.tick_params(axis='x', rotation=45)
    st.pyplot(fig6)