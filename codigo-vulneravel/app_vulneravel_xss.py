from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# Estilo visual vermelho para indicar perigo/vulnerabilidade (Contraste com o Seguro)
CSS_ESTILO = '''
<style>
    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #fff5f5; margin: 0; padding: 20px; }
    .container { max-width: 800px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
    h1 { color: #c92a2a; border-bottom: 2px solid #c92a2a; padding-bottom: 10px; display: flex; justify-content: space-between; align-items: center; }
    nav { margin-bottom: 20px; background: #c92a2a; padding: 10px; border-radius: 4px; }
    nav a { color: white; margin-right: 15px; text-decoration: none; font-weight: bold; }
    nav a:hover { text-decoration: underline; }
    .card { border: 1px solid #ffa8a8; padding: 15px; border-radius: 4px; background: #fff; margin-top: 20px; position: relative; }
    input[type="text"], textarea { width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ffc9c9; border-radius: 4px; box-sizing: border-box; background: #fff0f0; }
    input[type="submit"] { background-color: #c92a2a; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; }
    input[type="submit"]:hover { background-color: #a02323; }
    .danger-badge { background: #c92a2a; color: white; padding: 4px 12px; border-radius: 20px; font-size: 14px; text-transform: uppercase; }
    .debug-box { background: #fff5f5; border: 1px dashed #c92a2a; padding: 15px; margin-top: 30px; font-family: 'Courier New', Courier, monospace; font-size: 13px; color: #c92a2a; border-radius: 4px; }
    .comment-header { font-size: 12px; color: #fa5252; margin-bottom: 5px; font-weight: bold; }
</style>
'''

# Template base centralizado
LAYOUT_BASE = f'''
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Sprint 2 - Lab XSS Vulnerável</title>
    {CSS_ESTILO}
</head>
<body>
    <div class="container">
        <h1>Sistema Vulnerável <span class="danger-badge">Vulnerável</span></h1>
        <nav>
            <a href="/">Início</a>
            <a href="/reflected?nome=Convidado">Reflected XSS</a>
            <a href="/stored">Stored XSS</a>
        </nav>
        {{{{ conteudo | safe }}}}
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    html_home = '''
    <h3>Laboratório de Exploração de Vulnerabilidades</h3>
    <p>Esta aplicação foi desenvolvida para fins educacionais e contém falhas críticas de <b>Cross-Site Scripting (XSS)</b>.</p>
    <p>Utilize o menu superior para navegar entre os pontos de injeção e realizar os testes documentados no guia.</p>
    <div class="card" style="border-left: 5px solid #c92a2a;">
        <strong>Atenção:</strong> Esta versão utiliza interpolação direta de strings, permitindo que o navegador execute qualquer script injetado.
    </div>
    '''
    return render_template_string(LAYOUT_BASE, conteudo=html_home)

@app.route('/reflected')
def reflected_xss():
    nome = request.args.get('nome', '')
    
    # VULNERÁVEL: O nome é inserido diretamente no HTML sem sanitização
    html_reflected = f'''
    <h3>Ponto de Injeção: Reflected XSS</h3>
    <div class="card">
        <p>Bem-vindo ao sistema, <b>{nome}</b>!</p>
        <hr>
        <small>O parâmetro <code>nome</code> da URL está sendo refletido acima.</small>
    </div>
    
    <div class="debug-box">
        <strong>[LOG DO SERVIDOR] HTML Renderizado:</strong><br>
        &lt;p&gt;Bem-vindo ao sistema, &lt;b&gt;{nome}&lt;/b&gt;!&lt;/p&gt;
    </div>
    '''
    return render_template_string(LAYOUT_BASE, conteudo=html_reflected)

@app.route('/stored', methods=['GET', 'POST'])
def stored_xss():
    conn = sqlite3.connect('app_xss.db')
    cursor = conn.cursor()
    
    if request.method == 'POST':
        texto = request.form.get('texto', '')
        # Salva o comentário sem nenhum tratamento de segurança
        cursor.execute("INSERT INTO comentarios (usuario_id, texto) VALUES (1, ?)", (texto,))
        conn.commit()
    
    cursor.execute("SELECT id, texto, data_criacao FROM comentarios ORDER BY id DESC")
    comentarios = cursor.fetchall()
    conn.close()
    
    html_comentarios = '''
    <h3>Ponto de Injeção: Stored XSS</h3>
    <div class="card">
        <form method="post">
            <label>Deixe um comentário (Aceita HTML/Scripts):</label>
            <textarea name="texto" placeholder="<script>alert('XSS')</script>" rows="4"></textarea>
            <input type="submit" value="Publicar no Mural">
        </form>
    </div>
    <br>
    <h4>Mural da Comunidade</h4>
    '''
    
    for c in comentarios:
        # VULNERÁVEL: Cada comentário do banco é injetado diretamente como HTML
        html_comentarios += f'''
        <div class="card">
            <div class="comment-header">ID: #{c[0]} | Postado em: {c[2]}</div>
            {c[1]}
        </div>
        '''
    
    return render_template_string(LAYOUT_BASE, conteudo=html_comentarios)

if __name__ == '__main__':
    # Porta 5000 padrão para a versão vulnerável
    app.run(debug=True, port=5000)