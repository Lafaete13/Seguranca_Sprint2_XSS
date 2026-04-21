from flask import Flask, request, render_template_string
import sqlite3
import html  # Biblioteca essencial para defesa contra XSS

app = Flask(__name__)

# Estilo visual verde para diferenciar da aplicação vulnerável (Defesa)
CSS_ESTILO = '''
<style>
    body { font-family: 'Segoe UI', sans-serif; background-color: #e8f5e9; margin: 0; padding: 20px; }
    .container { max-width: 800px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
    h1 { color: #2e7d32; border-bottom: 2px solid #2e7d32; padding-bottom: 10px; }
    nav { margin-bottom: 20px; background: #1b5e20; padding: 10px; border-radius: 4px; }
    nav a { color: white; margin-right: 15px; text-decoration: none; font-weight: bold; }
    .card { border: 1px solid #c8e6c9; padding: 15px; border-radius: 4px; background: #fff; margin-top: 20px; }
    input[type="text"], textarea { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
    input[type="submit"] { background-color: #2e7d32; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
    .safe-badge { display: inline-block; background: #2e7d32; color: white; padding: 2px 8px; border-radius: 10px; font-size: 12px; }
    .debug-query { background: #e8f5e9; border: 1px solid #2e7d32; padding: 10px; margin-top: 20px; font-family: monospace; font-size: 12px; color: #1b5e20; }
</style>
'''

# Template base utilizando uma variável {{ conteudo }} em vez de blocos Jinja2
# Isso evita o erro "block defined twice" ao usar render_template_string
LAYOUT_BASE = f'''
<!DOCTYPE html>
<html>
<head><title>Sprint 2 - XSS Seguro</title>{CSS_ESTILO}</head>
<body>
    <div class="container">
        <h1>Sistema Seguro <span class="safe-badge">PROTEGIDO</span></h1>
        <nav>
            <a href="/">Início</a>
            <a href="/reflected?nome=Estudante">XSS Refletido</a>
            <a href="/stored">XSS Armazenado</a>
        </nav>
        {{{{ conteudo | safe }}}}
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    html_home = '''
    <h3>Bem-vindo à Versão Segura</h3>
    <p>Nesta aplicação, todas as entradas de usuário são tratadas com <b>HTML Escaping</b>.</p>
    <p>Tente utilizar os mesmos payloads da versão vulnerável para testar a defesa.</p>
    '''
    return render_template_string(LAYOUT_BASE, conteudo=html_home)

@app.route('/reflected')
def reflected_xss_seguro():
    nome = request.args.get('nome', '')
    
    # DEFESA: html.escape neutraliza scripts
    nome_seguro = html.escape(nome)
    
    html_reflected = f'''
    <h3>Página de Boas-vindas</h3>
    <div class="card">
        <p>Olá, <b>{nome_seguro}</b>!</p>
        <hr>
        <small>Nota: O script injetado foi transformado em texto literal.</small>
    </div>
    <div class="debug-query">
        <strong>Conteúdo processado:</strong> {nome_seguro}
    </div>
    '''
    return render_template_string(LAYOUT_BASE, conteudo=html_reflected)

@app.route('/stored', methods=['GET', 'POST'])
def stored_xss_seguro():
    conn = sqlite3.connect('app_xss.db')
    cursor = conn.cursor()
    
    if request.method == 'POST':
        comentario = request.form.get('texto', '')
        # Defesa contra SQLi (Prepared Statement)
        cursor.execute("INSERT INTO comentarios (usuario_id, texto) VALUES (1, ?)", (comentario,))
        conn.commit()
    
    cursor.execute("SELECT texto FROM comentarios")
    comentarios = cursor.fetchall()
    conn.close()
    
    # Construção da lista de comentários com escape
    html_corpo = '''
    <h3>Mural de Comentários Seguro</h3>
    <form method="post">
        <textarea name="texto" placeholder="Tente injetar um script..." rows="4"></textarea>
        <input type="submit" value="Postar Comentário">
    </form>
    '''
    
    for c in comentarios:
        # DEFESA: Escapar cada comentário vindo do banco antes de mostrar na tela
        texto_seguro = html.escape(c[0]) 
        html_corpo += f'<div class="card">{texto_seguro}</div>'
    
    return render_template_string(LAYOUT_BASE, conteudo=html_corpo)

if __name__ == '__main__':
    # Rodando na porta 5001 para não conflitar com a versão vulnerável
    app.run(debug=True, port=5001)