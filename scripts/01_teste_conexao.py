import pandas as pd
import os

# 1. Definir o caminho relativo para a pasta Bronze. 
# Como o script está na pasta "scripts/", usamos "../" para voltar uma pasta e entrar em "dados/"
CAMINHO_BRONZE = "../dados/1_bronze_raw/"

# 2. Listar os arquivos para garantir que o Python os encontra
print("Arquivos encontrados na camada Bronze:")
try:
    print(os.listdir(CAMINHO_BRONZE))
except FileNotFoundError:
    print("Aviso: A pasta Bronze ainda não foi encontrada. Verifique se você está executando o script do lugar certo.")

print("-" * 50)

# 3. Ler a tabela de clientes para testar a ingestão
nome_arquivo_clientes = "olist_customers_dataset.csv"
caminho_completo = os.path.join(CAMINHO_BRONZE, nome_arquivo_clientes)

try:
    df_clientes = pd.read_csv(caminho_completo)
    print("\n✅ Sucesso! Camada Bronze conectada com sucesso.")
    print(f"Total de clientes importados para a memória: {df_clientes.shape[0]} linhas")
    
    # Mostrar as 5 primeiras linhas do dado bruto para validação
    print("\nVisualização dos dados brutos (Bronze):")
    print(df_clientes.head())
    
except FileNotFoundError:
    print(f"\n❌ Erro: O arquivo '{nome_arquivo_clientes}' não foi encontrado.")
    print("Verifique se ele foi descompactado e colocado dentro de 'dados/1_bronze_raw/'")