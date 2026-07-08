import hashlib
import re
import streamlit as st


def criptografar_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()


def validar_email(email):
    padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(padrao, email) is not None


def logout():
    st.session_state.logado = False
    st.session_state.usuario = {}
    st.rerun()


def verificar_login():

    if "logado" not in st.session_state:
        st.session_state.logado = False

    if not st.session_state.logado:
        st.switch_page("pages/usuario.py")