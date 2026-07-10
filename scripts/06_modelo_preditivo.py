import pandas as pd
import sqlite3
import os
from sklearn.linear_model import LinearRegression

# 1. Caminho do banco de dados Gold
CAMINHO_GOLD = "../dados/3_gold_refined/"
caminho_banco = os.path.join(CAMINHO_GOLD, "ecommerce_olist.db")

print("Iniciando o treinamento do Modelo Preditivo (IA)...\n")

try:
    conexao = sqlite3.connect(caminho_banco)
    
    # 2. Buscar o faturamento agrupado por mês
    # O SQLite usa strftime para extrair o Ano e o Mês da data de compra
    query = """
        SELECT 
            strftime('%Y-%m', p.order_purchase_timestamp) as Mes,
            ROUND(SUM(i.price), 2) as Faturamento
        FROM pedidos p
        JOIN itens_pedido i ON p.order_id = i.order_id
        GROUP BY Mes
        ORDER BY Mes
    """
    df_historico = pd.read_sql_query(query, conexao)
    
    # Remover linhas vazias (se houver)
    df_historico = df_historico.dropna()
    
    print("- Histórico de vendas carregado. Últimos 3 meses:")
    print(df_historico.tail(3))
    
    # 3. Preparando os dados para a IA (scikit-learn)
    # Modelos matemáticos precisam de números. Vamos criar um "Índice do Mês" (1, 2, 3...)
    df_historico['Indice_Mes'] = range(1, len(df_historico) + 1)
    
    # Separando o X e o y
    X = df_historico[['Indice_Mes']] # Feature (A variável que usamos para prever)
    y = df_historico['Faturamento']  # Target (O alvo que queremos acertar)
    
    # 4. Treinamento do Modelo (Regressão Linear)
    print("\n- Treinando o modelo de Machine Learning...")
    modelo = LinearRegression()
    modelo.fit(X, y) # É aqui que a "mágica" do aprendizado acontece!
    
    # 5. Prevendo o próximo mês
    proximo_indice = len(df_historico) + 1
    X_futuro = pd.DataFrame({'Indice_Mes': [proximo_indice]})
    
    previsao = modelo.predict(X_futuro)[0]
    
    print(f"\n✅ Modelo treinado com sucesso!")
    print(f"💰 Previsão de Faturamento para o próximo mês: R$ {previsao:,.2f}")
    
    # 6. Salvando a previsão no banco de dados para o nosso Dashboard usar
    df_previsao = pd.DataFrame({
        'Indicador': ['Previsão Proximo Mes'],
        'Valor_R$': [previsao]
    })
    df_previsao.to_sql('previsoes_ml', conexao, if_exists='replace', index=False)
    print("- Previsão salva no banco de dados (Tabela 'previsoes_ml').")

    conexao.close()

except Exception as e:
    print(f"\n❌ Ocorreu um erro: {e}")