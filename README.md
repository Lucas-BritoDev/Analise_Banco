# 📊 Dashboard Interativo de Análise de Dados Bancários

## 📝 Descrição

Este projeto apresenta um dashboard interativo construído com Streamlit para a análise de dados bancários. O objetivo é demonstrar um ciclo completo de análise de dados, desde a coleta e limpeza até a interpretação, visualização e sugestão de tomadas de decisão estratégica para uma instituição financeira fictícia.

Através deste dashboard, é possível explorar o perfil de clientes, segmentações, canais de atendimento, níveis de satisfação, rentabilidade e identificar oportunidades para melhorar a qualidade do atendimento e aumentar o lucro da instituição.

⚠️ **Importante:** Os dados utilizados nesta análise são **fictícios** e foram **gerados programaticamente com Python (NumPy, Pandas)** dentro do próprio script (`app.py`) para simular um ambiente bancário realista e permitir a exploração das funcionalidades de análise.

## ✨ Funcionalidades Principais

O dashboard está estruturado em 6 etapas principais de um projeto de análise de dados:

1.  🗂️ **Coleta de Dados:** Apresentação da origem simulada dos dados e uma amostra.
2.  🧹 **Limpeza de Dados:** Demonstração de verificações básicas de consistência e qualidade dos dados.
3.  📊 **Exploração de Dados (EDA):** Análises visuais interativas sobre:
    * Perfil dos Clientes (idade, tempo de relacionamento, saldo, nº de produtos)
    * Segmentação de Clientes (Varejo, Premium, Alta Renda, Private)
    * Canais de Atendimento (App, Agência, etc.)
    * Níveis de Satisfação
    * Rentabilidade
4.  🔍 **Análise e Interpretação Avançada:**
    * **Segmentação Avançada de Clientes:** Criação de segmentos baseados em valor (Saldo, Frequência, Valor de Transações).
    * **Análise de Atendimento:** Relação entre frequência de contatos, canais e satisfação.
    * **Modelos Preditivos (Simulados):** Estimativa de risco de churn e seu impacto financeiro.
    * **Análise de Oportunidades:** Identificação de potencial em cross-selling, migração de canais e reativação de clientes.
5.  📈 **Visualização e Relatórios:** Um resumo dos principais indicadores e gráficos chave.
6.  ✅ **Tomada de Decisão:** Recomendações estratégicas detalhadas baseadas nos insights gerados, cobrindo atendimento, vendas, retenção, custo-benefício e inovação.

## 💡 Insights Chave Gerados (a partir dos dados simulados)

* Identificação de segmentos de clientes mais e menos rentáveis.
* Correlação entre satisfação, número de produtos e rentabilidade.
* Impacto dos canais de atendimento nos custos e na satisfação do cliente.
* Estimativa de risco de churn e o valor financeiro associado.
* Quantificação de oportunidades de economia (ex: migração para canais digitais) e aumento de receita (ex: reativação de clientes, cross-selling).

## 🛠️ Tecnologias Utilizadas

* **Python:** Linguagem principal para desenvolvimento e geração de dados.
* **Streamlit:** Para a criação do dashboard interativo.
* **Pandas:** Para manipulação e análise de dados tabulares.
* **NumPy:** Para operações numéricas e geração de dados simulados.
* **Plotly (Express & Graph Objects):** Para a criação de gráficos interativos e visualizações avançadas.
* **Statsmodels:** Para análises estatísticas (utilizado implicitamente na geração de dados e em possíveis futuras expansões).
* **Dateutil:** Para manipulação de datas.


##  navegando no Dashboard

Após executar o comando `streamlit run app.py`:

* Utilize a barra lateral para entender mais sobre o projeto e as tecnologias.
* Navegue pelas seções principais no corpo do dashboard (1. Coleta de Dados, 2. Limpeza de Dados, etc.).
* Dentro das seções de "Exploração de Dados" e "Análise e Interpretação", utilize as abas para visualizar diferentes análises específicas.
* Interaja com os gráficos (passando o mouse sobre os dados, clicando em legendas para filtrar, etc.).
* Na seção "Coleta de Dados", há um botão para baixar os dados simulados em formato CSV.


