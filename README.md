📄 README PROFISSIONAL — Análise de Vendas e Performance (Dados Fictícios)
Dashboard completo para análise comercial de uma empresa fictícia do setor de eletrônicos
🚀 Demonstração ao vivo

👉 Acesse o dashboard diretamente na nuvem (Streamlit Cloud):
🔗 https://wellsoleralves-an-lise-de-performance-de-vendas-app-fmyetu.streamlit.app/

📊 Sobre o projeto

Este projeto simula uma operação completa de vendas de uma empresa fictícia de eletrônicos, cobrindo:

geração de dados sintéticos realistas

criação de metas mensais por estado e canal

construção de um dashboard moderno em Streamlit

análises de performance, lucratividade e comportamento comercial

O objetivo é demonstrar, em um único repositório, competências em Python, análise de dados, modelagem, geração de datasets, construção de dashboards web e deploy na nuvem.

⭐ Principais funcionalidades
✔ 1. Geração de dados fictícios realistas

O script generate_data.py produz automaticamente:

8.000 registros de pedidos

informações financeiras (receita, custo, lucro, margem)

descontos, categorias, marcas e composição do pedido

metas mensais automáticas por estado e canal

Os arquivos gerados são salvos em:

data/sales_data.csv
data/monthly_targets.csv

✔ 2. Dashboard interativo em Streamlit

O app.py disponibiliza:

🔎 Filtros dinâmicos

Período

Estado

Cidade

Canal

Categoria

Marca

📈 KPIs e indicadores automáticos

Receita total

Lucro

Margem

Ticket médio

Volume de vendas

📊 Visualizações

Vendas por período

Margem por categoria

Distribuição por estado

Comparação de metas vs. realizado

Curvas de tendência e sazonalidade

✔ 3. Tabela “Top Produtos” com exportação em CSV

Uma das funcionalidades chave do dashboard é a tabela Top Produtos, que permite:

listar automaticamente os produtos mais vendidos em receita ou volume

aplicar filtros personalizados

gerar e baixar um relatório em formato CSV diretamente pelo navegador

Essa função é extremamente útil para operações comerciais, BI e análises rápidas.

🛠 Tecnologias utilizadas

Python 3.11+

Streamlit

Pandas

NumPy

Altair / Plotly (para gráficos)

Git + GitHub

Streamlit Cloud (deploy)

📁 Estrutura do repositório
.
├── app.py                     # Dashboard Streamlit
├── generate_data.py           # Script para gerar dados fictícios
├── requirements.txt           # Dependências para execução
├── data/
│   ├── sales_data.csv         # Base de pedidos gerada automaticamente
│   └── monthly_targets.csv    # Metas mensais
└── assets/
    └── logo.svg               # Logotipo usado no dashboard

🖥 Como rodar localmente
1. Criar ambiente virtual (opcional, mas recomendado)
python -m venv .venv
.\.venv\Scripts\Activate

2. Instalar dependências
pip install -r requirements.txt

3. Gerar os dados fictícios
python generate_data.py

4. Executar o dashboard
streamlit run app.py

📈 Habilidades demonstradas neste projeto

Construção de dashboards web profissionais com Streamlit

Geração programática de datasets sintéticos realistas

Processamento de dados para análises comerciais

Deploy e versionamento em GitHub

Publicação e hospedagem no Streamlit Cloud

Uso de filtros dinâmicos, KPIs, gráficos e exportação CSV

Organização de projeto em arquitetura clara e reprodutível

🎯 Por que este projeto é valioso para portfólio

Este repositório demonstra uma solução completa de dados + visualização + deploy, algo que empresas valorizam muito em profissionais de:

Business Intelligence

Análise de Dados

Engenharia de Dados

Desenvolvimento com Python

Criação de dashboards executivos

Projetos de automação e relatórios

O fato de o app estar rodando 100% online no Streamlit Cloud mostra domínio de infraestrutura leve e publicação de aplicações.

🔗 Acesso ao dashboard

👉 https://wellsoleralves-an-lise-de-performance-de-vendas-app-fmyetu.streamlit.app/
