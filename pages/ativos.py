import streamlit as st
import pandas as pd
from database import conn, cursor
from utils import verificar_login

verificar_login()

# ===============================
# CONFIGURAÇÃO
# ===============================

st.title("📦 Gestão de Ativos")
st.caption("Controle e acompanhamento dos equipamentos cadastrados")

st.divider()


# ===============================
# BUSCA
# ===============================

pesquisa = st.text_input(
    "🔎 Buscar ativo",
    placeholder="Digite patrimônio ou nome do equipamento..."
)


# ===============================
# CONSULTA BANCO
# ===============================

cursor.execute("""
SELECT
nome,
categoria,
laboratorio,
status,
quantidade
FROM ativos
""")

dados = cursor.fetchall()


df = pd.DataFrame(
    dados,
    columns=[
        "Nome",
        "Categoria",
        "Laboratório",
        "Status",
        "Quantidade"
    ]
)


# FILTRO

if pesquisa:

    pesquisa = pesquisa.lower()

    df = df[
        df["Nome"].str.lower().str.contains(
            pesquisa,
            na=False
        )]

# ===============================
# INDICADORES
# ===============================

total = len(df)

disponiveis = len(
    df[df["Status"] == "Disponível"]
)

manutencao = len(
    df[df["Status"] == "Em manutenção"]
)


c1, c2, c3 = st.columns(3)


with c1:
    st.metric(
        "📦 Total de equipamentos",
        total
    )


with c2:
    st.metric(
        "✅ Disponíveis",
        disponiveis
    )


with c3:
    st.metric(
        "🔧 Manutenção",
        manutencao
    )


st.divider()


# ===============================
# LISTAGEM
# ===============================


st.subheader("Equipamentos cadastrados")


with st.container(border=True):

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        height=400,
        column_config={

            "Status": st.column_config.TextColumn(
                "Situação"
            ),

            "Quantidade": st.column_config.NumberColumn(
                "Qtd."
            )
        }
    )


# ===============================
# RESUMO
# ===============================

st.caption(
    f"Total exibido: {len(df)} equipamento(s)"
)

from utils import logout

if st.sidebar.button("Sair"):
    logout()