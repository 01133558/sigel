import streamlit as st
from database import conn, cursor
from utils import verificar_login

verificar_login()

st.title("🤖 Assistente")
st.caption("Faça perguntas simples sobre os ativos cadastrados.")

with st.expander("💡 Exemplos de perguntas", expanded=True):

    st.markdown("""
- 📦 Quantos ativos existem?
- ✅ Quantos ativos estão disponíveis?
- 🔧 Quantos ativos estão em manutenção?
- 👨‍💻 Quantos ativos estão em uso?
- 📋 Listar ativos
- 🏢 Ativos por laboratório
- 🖥️ Ativos por categoria
""")

pergunta = st.chat_input("Digite sua pergunta...")

if pergunta:

    with st.chat_message("user"):
        st.write(pergunta)

    texto = pergunta.lower()

    resposta = ""

    # -----------------------------
    # Total de ativos
    # -----------------------------
    if "total" in texto or "quantos ativos" in texto:

        cursor.execute("SELECT SUM(quantidade) FROM ativos")
        total = cursor.fetchone()[0] or 0

        resposta = f"Existem **{total}** ativos cadastrados."

    # -----------------------------
    # Disponíveis
    # -----------------------------
    elif "dispon" in texto:

        cursor.execute("""
        SELECT SUM(quantidade)
        FROM ativos
        WHERE status='Disponível'
        """)

        total = cursor.fetchone()[0] or 0

        resposta = f"Existem **{total}** ativos disponíveis."

    # -----------------------------
    # Em manutenção
    # -----------------------------
    elif "manutenção" in texto or "manutencao" in texto:

        cursor.execute("""
        SELECT SUM(quantidade)
        FROM ativos
        WHERE status='Em manutenção'
        """)

        total = cursor.fetchone()[0] or 0

        resposta = f"Existem **{total}** ativos em manutenção."

    # -----------------------------
    # Em uso
    # -----------------------------
    elif "uso" in texto:

        cursor.execute("""
        SELECT SUM(quantidade)
        FROM ativos
        WHERE status='Em uso'
        """)

        total = cursor.fetchone()[0] or 0

        resposta = f"Existem **{total}** ativos em uso."

    # -----------------------------
    # Mostrar todos
    # -----------------------------
    elif "listar" in texto or "mostrar" in texto:

        cursor.execute("""
        SELECT nome,status
        FROM ativos
        ORDER BY nome
        """)

        dados = cursor.fetchall()

        if dados:

            resposta = "### Ativos cadastrados\n\n"

            for nome, status in dados:

                resposta += (
                    f"• **{nome}** "
                )

        else:

            resposta = "Nenhum ativo cadastrado."

    # -----------------------------
    # Laboratórios
    # -----------------------------
    elif "laboratório" in texto or "laboratorio" in texto:

        cursor.execute("""
        SELECT laboratorio,
               SUM(quantidade)
        FROM ativos
        GROUP BY laboratorio
        """)

        dados = cursor.fetchall()

        resposta = "### Ativos por laboratório\n\n"

        for lab, qtd in dados:

            resposta += f"• {lab}: **{qtd}** ativos\n"

    # -----------------------------
    # Categoria
    # -----------------------------
    elif "categoria" in texto:

        cursor.execute("""
        SELECT categoria,
               SUM(quantidade)
        FROM ativos
        GROUP BY categoria
        ORDER BY categoria
        """)

        dados = cursor.fetchall()

        resposta = "### Ativos por categoria\n\n"

        for categoria, qtd in dados:

            resposta += f"• {categoria}: **{qtd}**\n"

    else:

        resposta = """
Não consegui entender.

Você pode perguntar:

- Quantos ativos existem?
- Quantos estão disponíveis?
- Quantos estão em manutenção?
- Quantos estão em uso?
- Listar ativos
- Ativos por laboratório
- Ativos por categoria
"""

    with st.chat_message("assistant"):
        st.markdown(resposta)