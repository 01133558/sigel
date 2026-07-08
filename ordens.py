import streamlit as st
from datetime import datetime

from utils import verificar_login
from database import conn, cursor

verificar_login()

st.title("📋 Ordens de Serviço")
st.caption("Gerencie as ordens de manutenção dos ativos.")

# =====================================================
# MÉTRICAS
# =====================================================

cursor.execute("SELECT COUNT(*) FROM ordens")
total = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM ordens WHERE status='Aberta'")
abertas = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM ordens WHERE status='Em andamento'")
andamento = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM ordens WHERE status='Finalizada'")
finalizadas = cursor.fetchone()[0]

c1, c2, c3 = st.columns(3)

c1.metric("Total", total)
c2.metric("🔴 Abertas", abertas)
c3.metric("🟢 Finalizadas", finalizadas)

st.divider()

# =====================================================
# NOVA ORDEM
# =====================================================

with st.container(border=True):

    st.subheader("➕ Nova Ordem de Serviço")

    cursor.execute("""
    SELECT id, nome
    FROM ativos
    ORDER BY nome
    """)

    ativos = cursor.fetchall()

    lista_ativos = {nome: id for id, nome in ativos}

    col1, col2 = st.columns(2)

    with col1:

        ativo = st.selectbox(
            "Ativo",
            options=list(lista_ativos.keys())
        )

        tecnico = st.text_input("Técnico")

        prioridade = st.selectbox(
            "Prioridade",
            ["Baixa", "Média", "Alta"]
        )

    with col2:

        status = st.selectbox(
            "Status",
            [
                "Aberta",
                "Em andamento",
                "Finalizada"
            ]
        )

        problema = st.text_area(
            "Problema",
            height=120
        )

    observacoes = st.text_area(
        "Observações",
        height=80
    )

    if st.button(
        "💾 Salvar Ordem",
        use_container_width=True
    ):

        if tecnico == "" or problema == "":

            st.warning("Preencha os campos obrigatórios.")

        else:

            cursor.execute("""
            INSERT INTO ordens(
                ativo_id,
                tecnico,
                problema,
                observacoes,
                prioridade,
                status,
                data_abertura
            )
            VALUES(?,?,?,?,?,?,?)
            """, (

                lista_ativos[ativo],
                tecnico,
                problema,
                observacoes,
                prioridade,
                status,
                datetime.now().strftime("%d/%m/%Y %H:%M")

            ))

            conn.commit()

            st.success("Ordem cadastrada com sucesso!")

            st.rerun()

st.divider()

# =====================================================
# HISTÓRICO
# =====================================================

st.subheader("📄 Histórico de Ordens")

pesquisa = st.text_input(
    "🔎 Pesquisar por ativo ou técnico"
)

cursor.execute("""
SELECT
ordens.id,
ativos.nome,
ordens.tecnico,
ordens.prioridade,
ordens.status,
ordens.data_abertura
FROM ordens
INNER JOIN ativos
ON ativos.id = ordens.ativo_id
ORDER BY ordens.id DESC
""")

dados = cursor.fetchall()

if pesquisa:

    pesquisa = pesquisa.lower()

    dados = [

        linha

        for linha in dados

        if pesquisa in linha[1].lower()

        or pesquisa in linha[2].lower()

    ]

st.dataframe(

    dados,

    use_container_width=True,

    hide_index=True,

    column_config={

        1: "ID",

        2: "Ativo",

        3: "Técnico",

        4: "Prioridade",

        5: "Status",

        6: "Data"

    }

)

from utils import logout

if st.sidebar.button("Sair"):
    logout()