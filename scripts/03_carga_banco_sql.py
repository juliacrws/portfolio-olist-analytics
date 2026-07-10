import pandas as pd
import sqlite3
import os

# 1. Definir os caminhos
CAMINHO_BRONZE = "../dados/1_bronze_raw/"
CAMINHO_SILVER = "../dados/2_silver_trusted/"
CAMINHO_GOLD = "../dados/3_gold_refined/"

# Criar a pasta Gold se não existir
os.makedirs(CAMINHO_GOLD, exist_ok=True)

print("Iniciando a carga de dados para o Banco de Dados SQL (Camada Gold)...\n")

# 2. Carregar os dados que já temos no Python (Pandas)
try:
    print("- Lendo arquivos CSV...")
    df_clientes = pd.read_csv(os.path.join(CAMINHO_BRONZE, "olist_customers_dataset.csv"))
    df_pedidos_limpos = pd.read_csv(os.path.join(CAMINHO_SILVER, "pedidos_limpos.csv"))
    
    # 3. Criar a conexão com o banco de dados SQLite
    # O arquivo .db será criado automaticamente na pasta Gold
    caminho_banco = os.path.join(CAMINHO_GOLD, "ecommerce_olist.db")
    conexao = sqlite3.connect(caminho_banco)
    print("- Conexão com o banco de dados estabelecida.")

    # 4. Enviar os dados do Pandas direto para tabelas SQL (Carga)
    print("- Criando e populando a tabela 'clientes'...")
    df_clientes.to_sql('clientes', conexao, if_exists='replace', index=False)
    
    print("- Criando e populando a tabela 'pedidos'...")
    df_pedidos_limpos.to_sql('pedidos', conexao, if_exists='replace', index=False)
    
    print(f"\n✅ Carga concluída com sucesso! Banco de dados criado em: {caminho_banco}")
    
    # 5. Opcional: Fazer uma consulta (Query) de teste para provar que funcionou
    query_teste = """
        SELECT customer_state as Estado, COUNT(customer_id) as Total_Clientes
        FROM clientes
        GROUP BY customer_state
        ORDER BY Total_Clientes DESC
        LIMIT 5;
    """
    print("\n📊 Top 5 Estados com mais clientes (Query SQL executada direto do Banco):")
    df_resultado = pd.read_sql_query(query_teste, conexao)
    print(df_resultado)

    # Fechar a conexão (boa prática de engenharia)
    conexao.close()

except Exception as e:
    print(f"\n❌ Ocorreu um erro: {e}")