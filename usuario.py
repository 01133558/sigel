import streamlit as st
import hashlib
import os
from database import conn, cursor
from config import PASTA_FOTOS
from utils import criptografar_senha
from utils import validar_email

# ==========================
# PASTA DAS FOTOS
# ==========================

os.makedirs(PASTA_FOTOS, exist_ok=True)

# ==========================
# SESSION
# ==========================

if "logado" not in st.session_state:
    st.session_state.logado = False

if "usuario" not in st.session_state:
    st.session_state.usuario = {}   

# ==========================
# FUNÇÕES
# ==========================

def cadastrar(nome, email, senha, foto):

    cursor.execute(
        "SELECT id FROM funcionarios WHERE email=?",
        (email,)
    )

    if cursor.fetchone():
        return False, "Este e-mail já está cadastrado."

    senha_hash = criptografar_senha(senha)

    caminho_foto = None

    if foto is not None:

        extensao = foto.name.split(".")[-1]

        nome_arquivo = (
            email.replace("@", "_")
            .replace(".", "_")
            + f".{extensao}"
        )

        caminho_foto = os.path.join(
            PASTA_FOTOS,
            nome_arquivo
        )

        with open(caminho_foto, "wb") as f:
            f.write(foto.getbuffer())

    cursor.execute("""
        INSERT INTO funcionarios
        (nome, email, senha, foto)
        VALUES (?, ?, ?, ?)
    """, (
        nome,
        email,
        senha_hash,
        caminho_foto
    ))

    conn.commit()

    return True, "Cadastro realizado com sucesso."


def login(email, senha):

    cursor.execute("""
        SELECT nome, senha, foto
        FROM funcionarios
        WHERE email=?
    """, (email,))

    usuario = cursor.fetchone()

    if usuario is None:
        return False

    if criptografar_senha(senha) != usuario[1]:
        return False

    st.session_state.logado = True

    st.session_state.usuario = {
        "nome": usuario[0],
        "email": email,
        "foto": usuario[2]
    }

    return True


# ==========================
# TELA
# ==========================



col1, col2, col3 = st.columns([1,2,1])

with col1: 
    st.title("SIGEL")


with col2:
    st.header("Sistema de Gestão de Equipamentos e Laboratórios.")

    st.caption(
        "Controle de equipamentos, usuários e ordens de serviço."
    )

    aba_login, aba_cadastro = st.tabs(
        ["🔑 Login", "📝 Cadastro"]
    )

st.caption(
    "© 2026 - Sistema de Organização de Ativos"
)

# ==========================
# LOGIN
# ==========================

with aba_login:

    email_login = st.text_input("E-mail")

    senha_login = st.text_input(
        "Senha",
        type="password"
    )

    st.button(
        "Entrar",
        use_container_width=True
    )

    if login(email_login, senha_login):

        st.success("Login realizado com sucesso!")
        st.rerun()

    else:

        st.error("E-mail ou senha inválidos.")

# ==========================
# CADASTRO
# ==========================

with aba_cadastro:

    nome = st.text_input("Nome completo")

    email = st.text_input(
        "E-mail",
        key="cad_email"
    )

    senha = st.text_input(
        "Senha",
        type="password",
        key="cad_senha"
    )

    foto = st.file_uploader(
        "Foto",
        type=["png", "jpg", "jpeg"]
    )

    if st.button(
        "Cadastrar",
        use_container_width=True
    ):

        if nome == "" or email == "" or senha == "":

            st.warning("Preencha todos os campos.")

        elif not validar_email(email):

            st.error("Digite um e-mail válido.")

        else:

            ok, mensagem = cadastrar(
                nome,
                email,
                senha,
                foto
            )

            if ok:
                st.success(mensagem)
            else:
                st.error(mensagem)

