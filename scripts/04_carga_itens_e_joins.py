import pandas as pd
import sqlite3
import os

# Caminhos
CAMINHO_BRONZE = "../dados/1_bronze_raw/"
CAMINHO_GOLD = "../dados/3_gold_refined/"
caminho_banco = os.path.join(CAMINHO_GOLD, "ecommerce_olist.db")

print("Iniciando a carga dos Itens dos Pedidos...\n")

try:
    # 1. Lendo os itens da camada Bronze (aqui os dados já vêm limpos o suficiente para o nosso escopo)
    df_itens = pd.read_csv(os.path.join(CAMINHO_BRONZE, "olist_order_items_dataset.csv"))
    
    # 2. Conectando ao banco Gold
    conexao = sqlite3.connect(caminho_banco)
    
    # 3. Adicionando a nova tabela ao nosso banco de dados
    print("- Criando e populando a tabela 'itens_pedido'...")
    df_itens.to_sql('itens_pedido', conexao, if_exists='replace', index=False)
    print("✅ Tabela de itens carregada com sucesso!")
    
    # 4. A Mágica do JOIN: Cruzando Clientes + Pedidos + Preços
    # Vamos descobrir qual estado traz mais DINHEIRO, não apenas quantidade de clientes.
    query_faturamento = """
        SELECT 
            c.customer_state as Estado,
            COUNT(DISTINCT p.order_id) as Total_Pedidos,
            ROUND(SUM(i.price), 2) as Faturamento_Total_R$
        FROM clientes c
        JOIN pedidos p ON c.customer_id = p.customer_id
        JOIN itens_pedido i ON p.order_id = i.order_id
        GROUP BY c.customer_state
        ORDER BY Faturamento_Total_R$ DESC
        LIMIT 5;
    """
    
    print("\n📊 Top 5 Estados que mais trazem receita (Query SQL Avançada com JOIN):")
    df_faturamento = pd.read_sql_query(query_faturamento, conexao)
    print(df_faturamento)

    conexao.close()

except Exception as e:
    print(f"\n❌ Ocorreu um erro: {e}")