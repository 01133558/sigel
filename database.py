import sqlite3

conn = sqlite3.connect(
    "database.db",
    check_same_thread=False
)

cursor = conn.cursor()

# =====================================================
# FUNCIONÁRIOS
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS funcionarios(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL,
    foto TEXT
)
""")

# =====================================================
# ATIVOS
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS ativos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT UNIQUE,
    categoria TEXT,
    fabricante TEXT,
    numero_serie TEXT,
    laboratorio TEXT,
    localizacao TEXT,
    status TEXT,
    quantidade INTEGER,
    data_cadastro TEXT,
    observacoes TEXT
)
""")

# =====================================================
# ORDENS DE SERVIÇO
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS ordens(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ativo_id INTEGER,
    tecnico TEXT,
    problema TEXT,
    observacoes TEXT,
    prioridade TEXT,
    status TEXT,
    data_abertura TEXT,

    FOREIGN KEY (ativo_id)
    REFERENCES ativos(id)
)
""")

# =====================================================
# MOVIMENTAÇÕES
# =====================================================

from datetime import datetime

def registrar_movimentacao(tipo, descricao, usuario="Sistema"):

    cursor.execute("""
    INSERT INTO movimentacoes(
        tipo,
        descricao,
        usuario,
        data
    )
    VALUES(?,?,?,?)
    """,(

        tipo,
        descricao,
        usuario,
        datetime.now().strftime("%d/%m/%Y %H:%M")

    ))

    conn.commit()

# =====================================================
# FUNÇÕES PARA ORDENS
# =====================================================

def listar_ativos():

    cursor.execute("""
    SELECT id, nome
    FROM ativos
    ORDER BY nome
    """)

    return cursor.fetchall()


def listar_ordens():

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

    return cursor.fetchall()


# =====================================================
# FUNÇÕES PARA MOVIMENTAÇÕES
# =====================================================

def listar_movimentacoes():

    cursor.execute("""
    SELECT
        movimentacoes.id,
        ativos.nome,
        movimentacoes.origem,
        movimentacoes.destino,
        movimentacoes.responsavel,
        movimentacoes.quantidade,
        movimentacoes.data_movimentacao

    FROM movimentacoes

    INNER JOIN ativos
    ON ativos.id = movimentacoes.ativo_id

    ORDER BY movimentacoes.id DESC
    """)

    return cursor.fetchall()


def total_movimentacoes():

    cursor.execute("""
    SELECT COUNT(*)
    FROM movimentacoes
    """)

    return cursor.fetchone()[0]


def total_ordens():

    cursor.execute("""
    SELECT COUNT(*)
    FROM ordens
    """)

    return cursor.fetchone()[0]


def total_ordens_status(status):

    cursor.execute("""
    SELECT COUNT(*)
    FROM ordens
    WHERE status=?
    """, (status,))

    return cursor.fetchone()[0]