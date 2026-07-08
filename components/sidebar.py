import streamlit as st

def sidebar():
    st.sidebar.title("Menu")

    opcao = st.sidebar.radio(
        "Navegação",
        [
            "Dashboard",
            "Ativos",
            "Movimentações"
        ]
    )

    return opcao