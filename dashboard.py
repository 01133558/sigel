import streamlit as st
import sqlite3
from datetime import date
from database import conn, cursor
from utils import verificar_login


verificar_login()


# ===============================
# CONFIGURAÇÃO
# ===============================

st.set_page_config(
    page_title="Cadastro de Ativos",
    page_icon="📦",
    layout="wide"
)


# ===============================
# CABEÇALHO
# ===============================

st.title("📦 Cadastro de Ativos")
st.caption(
    "Registre e organize os equipamentos presentes nos laboratórios."
)

st.divider()



# ===============================
# FORMULÁRIO
# ===============================

with st.container(border=True):

    st.subheader("Informações do equipamento")


    col1, col2 = st.columns(2)


    with col1:

        nome = st.text_input(
            "Nome do equipamento",
            placeholder="Ex: Notebook Dell"
        )


        categoria = st.selectbox(
            "Categoria",
            [
                "Computador",
                "Notebook",
                "Ferramenta",
                "Instrumento",
                "Equipamento",
                "Outro"
            ]
        )


        laboratorio = st.text_input(
            "Laboratório"
        )


    with col2:

        fabricante = st.text_input(
            "Fabricante"
        )


        numero_serie = st.text_input(
            "Número de série"
        )


        status = st.selectbox(
            "Situação do equipamento",
            [
                "Disponível",
                "Em uso",
                "Em manutenção"
            ]
        )



# ===============================
# LOCALIZAÇÃO
# ===============================


with st.container(border=True):

    st.subheader("📍 Localização e controle")


    col1, col2, col3 = st.columns(3)


    with col1:

        localizacao = st.text_input(
            "Local onde está armazenado"
        )


    with col2:

        quantidade = st.number_input(
            "Quantidade",
            min_value=1,
            value=1
        )


    with col3:

        data = st.date_input(
            "Data de cadastro",
            value=date.today()
        )


    observacoes = st.text_area(
        "Observações adicionais",
        placeholder="Informações importantes sobre o equipamento..."
    )



# ===============================
# SALVAR
# ===============================


st.divider()


if st.button(
    "💾 Salvar equipamento",
    type="primary",
    use_container_width=True
):

    if nome == "":
        st.warning(
            "Preencha o nome do equipamento."
        )

    else:

        try:

            cursor.execute("""
            INSERT INTO ativos(
                nome,
                categoria,
                fabricante,
                numero_serie,
                laboratorio,
                localizacao,
                status,
                quantidade,
                data_cadastro,
                observacoes
            )
            VALUES(?,?,?,?,?,?,?,?,?,?)
            """,
            (
                nome,
                categoria,
                fabricante,
                numero_serie,
                laboratorio,
                localizacao,
                status,
                quantidade,
                str(data),
                observacoes
            ))


            conn.commit()


            st.success(
                "✅ Equipamento cadastrado com sucesso!"
            )


        except sqlite3.IntegrityError:

            st.error(
                "⚠ Já existe um equipamento utilizando esse patrimônio."
            )

            from utils import logout

if st.sidebar.button("Sair"):
    logout()