import streamlit as st


# ==========================
# SESSION
# ==========================

if "logado" not in st.session_state:
    st.session_state.logado = False

if "usuario" not in st.session_state:
    st.session_state.usuario = {}


# ==========================
# PÁGINAS
# ==========================

usuario = st.Page(
    "pages/usuario.py",
    title="Login",
    icon="👤",
    default=True
)


dashboard = st.Page(
    "pages/dashboard.py",
    title="Dashboard",
    icon="📊"
)


ativos = st.Page(
    "pages/ativos.py",
    title="Ativos",
    icon="📦"
)


ordens = st.Page(
    "pages/ordens.py",
    title="Ordens de Serviço",
    icon="🛠️"
)


movimentacoes = st.Page(
    "pages/movimentacoes.py",
    title="Movimentações",
    icon="🚚"
)

assistente = st.Page(
    "pages/assistente.py",
    title="Assistente IA",
    icon="🤖"
)


# ==========================
# NAVEGAÇÃO
# ==========================

if st.session_state.logado:

    pg = st.navigation(
        {
            "Sistema": [
                dashboard,
                ativos,
                ordens,
                movimentacoes,
                assistente
            ]
        }
    )

else:

    pg = st.navigation(
        [
            usuario
        ]
    )


pg.run()