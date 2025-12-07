# Análise de Vendas e Performance (dados fictícios)

Projeto para gerar uma base completa de vendas de uma empresa fictícia de eletrônicos (estados do Brasil) e visualizá-la em um dashboard Streamlit moderno.

## O que vem pronto
- `generate_data.py`: script que cria pedidos fictícios (vendas) e um arquivo de metas mensais por estado e canal.
- `data/`: recebe os CSVs `sales_data.csv` e `monthly_targets.csv` gerados pelo script.
- `app.py`: dashboard em Streamlit com filtros, KPIs, gráficos e comparação de meta vs. realizado.
- `requirements.txt`: dependências para rodar localmente.

## Como rodar
1. Crie e ative um ambiente virtual (opcional, mas recomendado):
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate
   ```
2. Instale as dependências:
   ```powershell
   pip install -r requirements.txt
   ```
3. Gere os dados fictícios (ajuste quantidade ou período se quiser):
   ```powershell
   python generate_data.py --records 9000 --start 2023-01-01 --end 2024-12-31
   ```
4. Suba o dashboard:
   ```powershell
   streamlit run app.py
   ```
   Abra o link local que o Streamlit mostrar (geralmente http://localhost:8501).

## Campos gerados (sales_data.csv)
- `pedido_id`: identificador fictício do pedido
- `data`, `ano`, `mes`, `ano_mes`, `trimestre`: datas e cortes de período
- `estado`, `regiao`, `cidade`: localização
- `canal`: E-commerce, Marketplace, Loja Física, Parceiros B2B
- `categoria`, `marca`, `produto`: mix de produtos/linhas
- `preco_unitario`, `quantidade`, `desconto`: condições do pedido
- `receita`, `custo`, `lucro`, `margem_pct`: métricas financeiras

## Metas (monthly_targets.csv)
Metas mensais de faturamento e pedidos por `ano_mes`, `estado` e `canal`, derivadas da base gerada para facilitar a comparação meta vs. realizado no dashboard.

## Ideias de uso
- Publicar no Git como portfólio de BI/análise de dados.
- Conectar o CSV a outras ferramentas (Power BI, Tableau) ou usar direto no Streamlit.
- Ajustar pesos por estado/canal no script para simular cenários específicos.
- Criar novas visões no dashboard (p. ex. curvas de sazonalidade, composição de desconto e margem).
