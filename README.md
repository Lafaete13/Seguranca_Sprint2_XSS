Artefato Sprint 2 - XSS (Cross-Site Scripting)

Este repositório contém a entrega prática da Sprint 2 da disciplina de Segurança em Aplicações (2026/1) do Instituto Federal de Brasília (IFB).

O objetivo deste projeto é demonstrar o funcionamento de ataques de SQL Injection e XSS, bem como a implementação das suas respetivas defesas utilizando Output Encoding.

👥 Integrantes do Grupo [5]

[Lafaete Dias Alves]

[Gustavo Santos]

[Danielle Ester]

[Sandro Nunes]

📂 Estrutura do Projeto

XSS_Grupo[5]_Sprint2/
├── codigo-vulneravel/      # Aplicação com falhas intencionais (Porta 5000)
│   ├── app_vulneravel_xss.py
│   └── setup_db_xss.py
├── codigo-corrigido/       # Aplicação protegida (Porta 5001)
│   ├── app_seguro_xss.py
│   └── setup_db_xss.py
└── README.md               # Este ficheiro de documentação


🛠️ Tecnologias Utilizadas

Linguagem: Python

Framework Web: Flask

Base de Dados: SQLite3

🚀 Como Executar o Projeto

1. Instalar Dependências

Certifica-te de que tens o Python instalado e instala o Flask:

pip install flask


2. Preparar as Bases de Dados

Entra em cada pasta e executa o script de criação da base de dados:

# Na pasta vulnerável
cd codigo-vulneravel
python setup_db_xss.py
cd ..

# Na pasta corrigida
cd codigo-corrigido
python setup_db_xss.py
cd ..


3. Rodar as Aplicações

Recomenda-se abrir dois terminais para rodar ambas simultaneamente:

Vulnerável: python codigo-vulneravel/app_vulneravel_xss.py (Aceder em https://www.google.com/search?q=http://127.0.0.1:5000)

Segura: python codigo-corrigido/app_seguro_xss.py (Aceder em https://www.google.com/search?q=http://127.0.0.1:5001)

🛡️ Pontos de Injeção e Ataques

Foram implementados dois tipos de XSS obrigatórios:

Reflected XSS: Localizado no parâmetro ?nome= da rota /reflected.

Payload de teste: <script>alert('XSS')</script>

Stored XSS: Localizado no mural de comentários da rota /stored.

Payload de teste: <img src=x onerror="alert('XSS')">

🔒 Correções Implementadas

As defesas foram baseadas na técnica de Output Encoding, utilizando a biblioteca nativa html.escape do Python para neutralizar caracteres especiais (<, >, ", ') antes da renderização no navegador.

Este projeto foi desenvolvido para fins estritamente educacionais.
