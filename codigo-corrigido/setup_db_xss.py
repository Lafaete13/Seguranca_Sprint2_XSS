import sqlite3

def init_db():
    conn = sqlite3.connect('app_xss.db')
    cursor = conn.cursor()
    
    # Tabela de usuários (conforme guia Seção 2.1.4)
    cursor.execute("DROP TABLE IF EXISTS usuarios")
    cursor.execute("""
        CREATE TABLE usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome VARCHAR(100),
            email VARCHAR(100),
            role VARCHAR(20) DEFAULT 'user'
        )
    """)
    
    # Dados de exemplo
    cursor.execute("INSERT INTO usuarios (nome, email, role) VALUES ('Maria Silva', 'maria@email.com', 'user')")
    cursor.execute("INSERT INTO usuarios (nome, email, role) VALUES ('João Santos', 'joao@email.com', 'user')")
    cursor.execute("INSERT INTO usuarios (nome, email, role) VALUES ('Admin', 'admin@email.com', 'admin')")
    
    # Tabela de comentários para Stored XSS
    cursor.execute("DROP TABLE IF EXISTS comentarios")
    cursor.execute("""
        CREATE TABLE comentarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            texto TEXT,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("INSERT INTO comentarios (usuario_id, texto) VALUES (1, 'Primeiro comentário')")
    
    conn.commit()
    conn.close()
    print("Banco de dados app_xss.db configurado com sucesso!")

if __name__ == "__main__":
    init_db()