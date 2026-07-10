import pandas as pd
import os

# 1. Definir caminhos
CAMINHO_BRONZE = "../dados/1_bronze_raw/"
CAMINHO_SILVER = "../dados/2_silver_trusted/"

# Certificar que a pasta Silver existe (se não existir, o Python cria)
os.makedirs(CAMINHO_SILVER, exist_ok=True)

print("Iniciando a transformação dos dados de Pedidos para a Camada Silver...\n")

try:
    # 2. Carregar os dados brutos de pedidos
    df_pedidos = pd.read_csv(os.path.join(CAMINHO_BRONZE, "olist_orders_dataset.csv"))
    
    # 3. TRANSFORMAÇÕES (O coração da Engenharia de Dados)
    
    # Transformação A: Verificar e remover linhas onde a data de aprovação do pedido está vazia (NaN)
    # Motivo: Se não tem data de aprovação, não podemos analisar o tempo de entrega.
    total_antes = len(df_pedidos)
    df_pedidos_limpo = df_pedidos.dropna(subset=['order_approved_at'])
    total_depois = len(df_pedidos_limpo)
    
    print(f"- Removidas {total_antes - total_depois} linhas sem data de aprovação.")
    
    # Transformação B: Converter as colunas de data (que vêm como texto) para o formato correto de data (datetime)
    # Motivo: Precisamos que o Python entenda que é data para fazermos cálculos futuros (ex: tempo médio de entrega)
    colunas_de_data = [
        'order_purchase_timestamp', 
        'order_approved_at', 
        'order_delivered_carrier_date', 
        'order_delivered_customer_date', 
        'order_estimated_delivery_date'
    ]
    
    for coluna in colunas_de_data:
        df_pedidos_limpo[coluna] = pd.to_datetime(df_pedidos_limpo[coluna])
        
    print("- Colunas de data convertidas com sucesso.")
    
    # 4. Salvar o resultado na Camada Silver
    # Salvar em .csv para facilitar a nossa visualização por enquanto
    caminho_salvamento = os.path.join(CAMINHO_SILVER, "pedidos_limpos.csv")
    df_pedidos_limpo.to_csv(caminho_salvamento, index=False)
    
    print(f"\n✅ Transformação concluída! Dados salvos na Camada Silver em: {caminho_salvamento}")
    print(f"Total de pedidos prontos para análise: {total_depois}")

except FileNotFoundError:
    print("\n❌ Erro: O arquivo 'olist_orders_dataset.csv' não foi encontrado na pasta Bronze.")