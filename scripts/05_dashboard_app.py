import streamlit as st
import pandas as pd
import sqlite3
import os

# 1. Configuração da página
st.set_page_config(page_title="Olist Analytics", page_icon="📈", layout="wide")

st.title("📊 Dashboard Executivo de Performance - Olist")
st.markdown("Acompanhamento de KPIs e Business Analytics Integrado com IA Preditiva.")

# 2. Caminho do banco Gold
CAMINHO_GOLD = "../dados/3_gold_refined/"
caminho_banco = os.path.join(CAMINHO_GOLD, "ecommerce_olist.db")

# 3. Função para carregar os dados (Analíticos + Inteligência Artificial)
@st.cache_data
def carregar_dados():
    conexao = sqlite3.connect(caminho_banco)
    
    # Query do Faturamento Real
    query_faturamento = """
        SELECT 
            c.customer_state as Estado,
            COUNT(DISTINCT p.order_id) as Total_Pedidos,
            ROUND(SUM(i.price), 2) as Faturamento_Total
        FROM clientes c
        JOIN pedidos p ON c.customer_id = p.customer_id
        JOIN itens_pedido i ON p.order_id = i.order_id
        GROUP BY c.customer_state
        ORDER BY Faturamento_Total DESC
    """
    df_estado = pd.read_sql_query(query_faturamento, conexao)
    
    # Query da Previsão da IA
    try:
        query_ia = "SELECT Valor_R$ FROM previsoes_ml WHERE Indicador = 'Previsão Proximo Mes'"
        df_prev = pd.read_sql_query(query_ia, conexao)
        previsao_valor = df_prev['Valor_R$'].iloc[0]
    except Exception:
        previsao_valor = 0.0
        
    conexao.close()
    return df_estado, previsao_valor

# 4. Construindo a interface visual
try:
    df_estado, previsao_valor = carregar_dados()

    st.subheader("Indicadores Chave (KPIs)")
    
    faturamento_global = df_estado['Faturamento_Total'].sum()
    pedidos_globais = df_estado['Total_Pedidos'].sum()
    ticket_medio = faturamento_global / pedidos_globais

    # Agora criamos 4 colunas para caber a previsão da IA
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Faturamento Total", f"R$ {faturamento_global:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    col2.metric("Total de Pedidos", f"{pedidos_globais:,}".replace(',', '.'))
    col3.metric("Ticket Médio", f"R$ {ticket_medio:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    
    # Card especial de Machine Learning
    col4.metric("🤖 Previsão IA (Próx. Mês)", f"R$ {previsao_valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))

    st.divider()

    st.subheader("Faturamento por Estado (Top 10)")
    df_top10 = df_estado.head(10).set_index('Estado')
    st.bar_chart(df_top10['Faturamento_Total'])

except Exception as e:
    st.error(f"Erro ao carregar a aplicação: {e}")