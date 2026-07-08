import streamlit as st
import pandas as pd
from database import cursor
from utils import verificar_login, logout

verificar_login()

st.title("📜 Histórico do Sistema")
st.caption("Acompanhe todas as ações realizadas no sistema.")

# ==========================================
# MÉTRICAS
# ==========================================

cursor.execute("SELECT COUNT(*) FROM movimentacoes")
total = cursor.fetchone()[0]

cursor.execute("""
SELECT COUNT(*)
FROM movimentacoes
WHERE DATE(data_movimentacao)=DATE('now')
""")
hoje = cursor.fetchone()[0]

c1, c2 = st.columns(2)

c1.metric("Total de Registros", total)
c2.metric("Registros Hoje", hoje)

st.divider()

# ==========================================
# PESQUISA
# ==========================================

pesquisa = st.text_input(
    "🔎 Pesquisar movimentação"
)

# ==========================================
# HISTÓRICO
# ==========================================

cursor.execute("""
SELECT
data_movimentacao,
responsavel,
observacoes
FROM movimentacoes
ORDER BY data_movimentacao DESC
""")

dados = cursor.fetchall()

df = pd.DataFrame(
    dados,
    columns=[
        "Data",
        "Responsável",
        "Descrição"
    ]
)

if pesquisa:

    pesquisa = pesquisa.lower()

    df = df[
        df["Responsável"].str.lower().str.contains(
            pesquisa,
            na=False
        )
        |
        df["Descrição"].str.lower().str.contains(
            pesquisa,
            na=False
        )
    ]

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
    height=500
)

if st.sidebar.button("Sair"):
    logout()