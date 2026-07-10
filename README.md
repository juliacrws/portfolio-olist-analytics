# 📈 Olist Performance Analytics & Predictive AI

De ponta a ponta, este projeto demonstra a construção de um pipeline de dados baseado na arquitetura medalhão (Bronze, Silver e Gold), integrando Engenharia de Dados, Modelagem SQL, Machine Learning e Business Intelligence.

## 🚀 Link do Dashboard Interativo
Clique no link abaixo para acessar a aplicação web e interagir com os dados na nuvem:
👉 **[Acessar o Dashboard Executivo](https://portfolio-olist-analytics-fkjxd3udgqvbvlohfhntdk.streamlit.app/)**

---

## 📋 Contexto do Desafio
O objetivo deste projeto é consolidar dados brutos de um e-commerce real (Olist), transformá-los e limpá-los para gerar insights estratégicos de negócios (KPIs de faturamento, volume de pedidos e ticket médio por estado) e prever o comportamento de receita do próximo período utilizando Inteligência Artificial.

## 🏗️ Arquitetura de Dados (Medalhão)
O pipeline foi estruturado para seguir as melhores práticas de mercado:
1. **Camada Bronze (Raw):** Ingestão e leitura dos datasets brutos em formato CSV.
2. **Camada Silver (Trusted):** Processamento, limpeza e conversão de tipos de dados (Data Cleansing) com tratamento de dados nulos e formatação de datas.
3. **Camada Gold (Refined):** Armazenamento relacional e estruturado utilizando tabelas dimensionais e fatos via **Smart SQL** (SQLite), permitindo consultas rápidas e JOINS complexos.

## 🤖 Modelo de Inteligência Artificial
Foi implementado um modelo de **Regressão Linear** (`scikit-learn`) que analisa a série histórica mensal de vendas para identificar tendências de crescimento e prever o faturamento estimado do próximo mês. O resultado preditivo é persistido no banco de dados para consumo da aplicação analítica.

## 🛠️ Tecnologias Utilizadas
- **Python 3** (Linguagem principal)
- **Pandas** (Engenharia de dados, ETL e manipulação)
- **SQLite3** (Banco de dados relacional e consultas SQL)
- **Scikit-learn** (Treinamento do modelo preditivo de Machine Learning)
- **Streamlit** (Desenvolvimento da aplicação web e visualização interativa)
- **Git & GitHub** (Versionamento de código)

---

## 🔧 Como Rodar o Projeto Localmente

Se quiser clonar este repositório e testar no seu computador, siga os passos abaixo:

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/juliacrws/portfolio-olist-analytics.git](https://github.com/juliacrws/portfolio-olist-analytics.git)
   cd portfolio-olist-analytics