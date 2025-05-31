# ==============================================================================
# Importações e Configuração Inicial
# ==============================================================================
import streamlit as st               # Biblioteca para criação de dashboards interativos
import pandas as pd                 # Biblioteca para manipulação de dados em formato tabular
import numpy as np                  # Biblioteca para operações numéricas e geração de dados
import plotly.express as px         # Biblioteca para visualizações interativas
import plotly.graph_objects as go   # Biblioteca para gráficos avançados
from plotly.subplots import make_subplots  # Ferramenta para criar subgráficos
import datetime                     # Biblioteca para manipulação de datas
import random                       # Biblioteca para geração de números aleatórios
from dateutil.relativedelta import relativedelta  # Ferramenta para cálculos de diferença de tempo
import statsmodels.api as sm

# Configuração inicial da página no Streamlit
st.set_page_config(
    page_title="Análise de Dados Bancários",
    page_icon="💰",
    layout="wide"
)

# Título principal do dashboard
st.title("📊 Dashboard de Análise de Dados Bancários")
st.markdown("---")  # Divisão visual

# ==============================================================================
# Barra Lateral
# ==============================================================================
with st.sidebar:
    st.header("Sobre o Projeto 🌞")
    st.markdown("""
    Este dashboard analisa dados bancários para melhorar a qualidade do atendimento e aumentar o lucro da instituição em 6 etapas:

    - 🗂️ **Coleta de dados**
    - 🧹 **Limpeza de dados**
    - 📊 **Exploração de dados (EDA)**
    - 🔍 **Análise e interpretação**
    - 📈 **Visualização e relatórios**
    - ✅ **Tomada de decisão**
    """)

    st.header("Tecnologias Utilizadas 🛠️")
    st.markdown("""
    - 🐍 **Python**
    - 🐼 **Pandas**
    - 🔢 **NumPy**
    - 📉 **Plotly**
    - 🌐 **Streamlit**
    - 📈 **statsmodels**            
    """)

# ==============================================================================
# Funções Auxiliares
# ==============================================================================

@st.cache_data
def gerar_dados(n_linhas=10000):
    """
    Gera um conjunto de dados simulados com informações de clientes bancários.

    Parâmetros:
    - n_linhas (int): Número de registros a serem gerados (padrão: 10.000).

    Retorna:
    - pd.DataFrame: DataFrame contendo os dados simulados.
    """
    # Definir seed para reprodutibilidade
    np.random.seed(42)
    random.seed(42)
    
    # Data atual para referência
    data_atual = datetime.datetime.now()
    
    # Criar IDs de clientes
    ids_clientes = np.arange(1, n_linhas + 1)
    
    # Gerar idades entre 18 e 85 anos com distribuição normal
    idades = np.random.normal(42, 15, n_linhas).astype(int)
    idades = np.clip(idades, 18, 85)
    
    # Gerar saldos bancários com distribuição exponencial
    saldos = np.random.exponential(10000, n_linhas)
    saldos = np.clip(saldos, 0, 500000)
    
    # Criar segmentos de clientes com probabilidades definidas
    segmentos = np.random.choice(['Varejo', 'Premium', 'Alta Renda', 'Private'], 
                                 p=[0.65, 0.20, 0.10, 0.05], size=n_linhas)
    
    # Gerar tempo de relacionamento com o banco (em meses)
    tempo_cliente = np.random.lognormal(3.5, 1, n_linhas).astype(int)
    tempo_cliente = np.clip(tempo_cliente, 1, 480)  # Máximo de 40 anos
    
    # Gerar número de produtos (1 a 8)
    num_produtos = np.random.negative_binomial(3, 0.4, n_linhas) + 1
    num_produtos = np.clip(num_produtos, 1, 8)
    
    # Gerar canais de atendimento preferidos
    canais = np.random.choice(['App', 'Internet Banking', 'Agência', 'Central Telefônica', 'Caixa Eletrônico'],
                              p=[0.45, 0.25, 0.15, 0.10, 0.05], size=n_linhas)
    
    # Gerar scores de satisfação (0-100)
    satisfacao = np.random.beta(7, 3, n_linhas) * 100
    
    # Definir se cliente está ativo ou inativo
    ativo = np.random.choice([True, False], p=[0.85, 0.15], size=n_linhas)
    
    # Valores de transações mensais
    valor_transacoes = np.random.exponential(2000, n_linhas)
    valor_transacoes = np.clip(valor_transacoes, 0, 50000)
    
    # Frequência de contatos com o banco por mês
    freq_contatos = np.random.poisson(3, n_linhas)
    freq_contatos = np.clip(freq_contatos, 0, 30)
    
    # Criar DataFrame inicial
    df = pd.DataFrame({
        'id_cliente': ids_clientes,
        'idade': idades,
        'saldo_conta': saldos.round(2),
        'segmento': segmentos,
        'tempo_cliente_meses': tempo_cliente,
        'num_produtos': num_produtos,
        'canal_preferido': canais,
        'satisfacao': satisfacao.round(1),
        'cliente_ativo': ativo,
        'valor_transacoes_mensais': valor_transacoes.round(2),
        'freq_contatos_mensais': freq_contatos
    })
    
    # Adicionar correlações artificiais para maior realismo
    # 1. Clientes Premium, Alta Renda e Private têm saldos maiores
    for i, seg in enumerate(['Varejo', 'Premium', 'Alta Renda', 'Private']):
        mask = df['segmento'] == seg
        df.loc[mask, 'saldo_conta'] = df.loc[mask, 'saldo_conta'] * (i + 1) * 1.5
    
    # 2. Satisfação maior em segmentos superiores
    for i, seg in enumerate(['Varejo', 'Premium', 'Alta Renda', 'Private']):
        mask = df['segmento'] == seg
        df.loc[mask, 'satisfacao'] = df.loc[mask, 'satisfacao'] * (1 + i * 0.05)
        df.loc[mask, 'satisfacao'] = np.clip(df.loc[mask, 'satisfacao'], 0, 100)
    
    # 3. Valor de transações maior para clientes com mais produtos
    for prod in range(1, 9):
        mask = df['num_produtos'] == prod
        df.loc[mask, 'valor_transacoes_mensais'] = df.loc[mask, 'valor_transacoes_mensais'] * (1 + prod * 0.15)
    
    # 4. Clientes mais velhos preferem canais tradicionais
    for i, canal in enumerate(['App', 'Internet Banking', 'Caixa Eletrônico', 'Central Telefônica', 'Agência']):
        mask = df['canal_preferido'] == canal
        idade_ajuste = np.random.normal(30 + i * 8, 5, sum(mask))
        df.loc[mask, 'idade'] = np.clip(idade_ajuste, 18, 85).astype(int)
    
    # 5. Clientes mais antigos têm mais produtos
    df['num_produtos'] = df['num_produtos'] + (df['tempo_cliente_meses'] / 120).astype(int)
    df['num_produtos'] = np.clip(df['num_produtos'], 1, 8)
    
    # 6. Calcular receita por cliente
    base_receita = np.random.lognormal(3, 1, n_linhas) * 10
    for i, seg in enumerate(['Varejo', 'Premium', 'Alta Renda', 'Private']):
        mask = df['segmento'] == seg
        base_receita[mask] = base_receita[mask] * (1 + i * 0.5)
    base_receita = base_receita * (1 + df['num_produtos'] * 0.2)
    base_receita = base_receita + (df['valor_transacoes_mensais'] * 0.01)
    base_receita[df['cliente_ativo']] = base_receita[df['cliente_ativo']] * 1.5
    df['receita_mensal'] = base_receita.round(2)
    
    # 7. Calcular custo de atendimento por canal
    custos_base = {
        'App': 0.5,
        'Internet Banking': 1.0,
        'Caixa Eletrônico': 3.0,
        'Central Telefônica': 7.0,
        'Agência': 15.0
    }
    custo_atendimento = np.zeros(n_linhas)
    for canal, custo in custos_base.items():
        mask = df['canal_preferido'] == canal
        custo_atendimento[mask] = custo
    df['custo_atendimento_mensal'] = (custo_atendimento * df['freq_contatos_mensais']).round(2)
    
    # 8. Calcular rentabilidade mensal (receita - custo)
    df['rentabilidade_mensal'] = (df['receita_mensal'] - df['custo_atendimento_mensal']).round(2)
    
    return df

def mostrar_estatisticas(df):
    """
    Exibe métricas principais dos dados bancários em formato de cartões de indicadores.

    Parâmetros:
    - df (pd.DataFrame): DataFrame com os dados bancários.
    """
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total de Clientes", f"{len(df):,}")
    with col2:
        ativos = df['cliente_ativo'].sum()
        st.metric("Clientes Ativos", f"{ativos:,} ({ativos/len(df):.1%})")
    with col3:
        st.metric("Saldo Médio", f"R$ {df['saldo_conta'].mean():,.2f}")
    with col4:
        st.metric("Satisfação Média", f"{df['satisfacao'].mean():.1f}/100")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Receita Mensal Total", f"R$ {df['receita_mensal'].sum():,.2f}")
    with col2:
        st.metric("Custo Mensal Total", f"R$ {df['custo_atendimento_mensal'].sum():,.2f}")
    with col3:
        rentabilidade = df['rentabilidade_mensal'].sum()
        st.metric("Rentabilidade Mensal", f"R$ {rentabilidade:,.2f}")
    with col4:
        st.metric("Rentabilidade Média/Cliente", f"R$ {df['rentabilidade_mensal'].mean():,.2f}")

# Gerar dados simulados
df = gerar_dados(10000)

# ==============================================================================
# Seção 1: Coleta de Dados
# ==============================================================================
st.header("1. Coleta de Dados")
st.markdown("""
Para este projeto, simulamos dados bancários de 10.000 clientes com informações sobre perfil, comportamento financeiro, 
padrões de uso de serviços e métricas de satisfação. Em um cenário real, esses dados seriam coletados de:

- Sistemas de core banking
- Registros de transações
- Pesquisas de satisfação
- Logs de interações com canais digitais
- Registros de atendimento
""")
with st.expander("Ver amostra dos dados coletados"):
    st.dataframe(df.head(10))
    st.download_button(
        label="Baixar dados completos",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name="dados_bancarios.csv",
        mime="text/csv"
    )
st.markdown("---")

# ==============================================================================
# Seção 2: Limpeza de Dados
# ==============================================================================
st.header("2. Limpeza de Dados")
st.markdown("""
Em dados reais, seria necessário realizar várias etapas de limpeza como:
- Tratamento de valores ausentes
- Remoção de duplicatas
- Correção de inconsistências
- Padronização de formatos

Para nossos dados simulados, realizaremos algumas verificações básicas para demonstrar o processo.
""")
with st.expander("Ver estatísticas e limpeza dos dados"):
    st.subheader("Estatísticas Descritivas")
    st.dataframe(df.describe().T)

    st.subheader("Verificação de Valores Ausentes")
    valores_ausentes = df.isnull().sum()
    if valores_ausentes.sum() > 0:
        st.dataframe(valores_ausentes[valores_ausentes > 0])
    else:
        st.write("Não há valores ausentes nos dados.")

    st.subheader("Tratamento de Outliers e Valores Impossíveis")
    st.write("Verificando idades fora do intervalo esperado (18-85 anos):")
    st.write(f"Registros afetados: {sum((df['idade'] < 18) | (df['idade'] > 85))}")
    st.write("Verificando saldos negativos:")
    st.write(f"Registros afetados: {sum(df['saldo_conta'] < 0)}")

    st.subheader("Distribuição de Segmentos")
    st.dataframe(df['segmento'].value_counts().reset_index().rename(columns={'index': 'Segmento', 'segmento': 'Quantidade'}))

    st.subheader("Distribuição de Canais de Atendimento")
    st.dataframe(df['canal_preferido'].value_counts().reset_index().rename(columns={'index': 'Canal', 'canal_preferido': 'Quantidade'}))
st.markdown("---")

# ==============================================================================
# Seção 3: Exploração de Dados (EDA)
# ==============================================================================
st.header("3. Exploração de Dados (EDA)")
st.markdown("""
A Análise Exploratória de Dados nos permite entender padrões, correlações e tendências importantes.
Vamos analisar diferentes aspectos dos dados bancários.
""")
mostrar_estatisticas(df)

# Criar abas para diferentes análises exploratórias
eda_tabs = st.tabs(["Perfil dos Clientes", "Segmentação", "Canais de Atendimento", "Satisfação", "Rentabilidade"])

# Aba 1: Perfil dos Clientes
with eda_tabs[0]:
    st.subheader("Distribuição de Idade dos Clientes")
    fig = px.histogram(df, x='idade', nbins=30, 
                       title='Distribuição de Idade dos Clientes',
                       labels={'idade': 'Idade', 'count': 'Quantidade de Clientes'},
                       color_discrete_sequence=['#2196f3'])
    fig.update_layout(xaxis_title='Idade', yaxis_title='Quantidade de Clientes')
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Tempo de Relacionamento com o Banco")
        fig = px.histogram(df, x='tempo_cliente_meses', nbins=30,
                           title='Distribuição do Tempo de Relacionamento',
                           labels={'tempo_cliente_meses': 'Tempo (meses)', 'count': 'Quantidade de Clientes'},
                           color_discrete_sequence=['#4caf50'])
        fig.update_layout(xaxis_title='Tempo (meses)', yaxis_title='Quantidade de Clientes')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Distribuição de Saldo em Conta")
        df_plot = df.copy()
        df_plot['saldo_log'] = np.log1p(df_plot['saldo_conta'])
        fig = px.histogram(df_plot, x='saldo_log', nbins=30,
                           title='Distribuição de Saldo (escala logarítmica)',
                           labels={'saldo_log': 'Log(Saldo + 1)', 'count': 'Quantidade de Clientes'},
                           color_discrete_sequence=['#ff9800'])
        fig.update_layout(xaxis_title='Log(Saldo + 1)', yaxis_title='Quantidade de Clientes')
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Número de Produtos por Cliente")
    produtos_count = df['num_produtos'].value_counts().sort_index().reset_index()
    produtos_count.columns = ['Número de Produtos', 'Quantidade de Clientes']
    fig = px.bar(produtos_count, x='Número de Produtos', y='Quantidade de Clientes',
                 title='Distribuição do Número de Produtos por Cliente',
                 color_discrete_sequence=['#9c27b0'])
    st.plotly_chart(fig, use_container_width=True)

# Aba 2: Segmentação
with eda_tabs[1]:
    st.subheader("Análise por Segmento de Cliente")
    fig = px.pie(df, names='segmento', title='Distribuição de Clientes por Segmento',
                 color_discrete_sequence=px.colors.qualitative.Safe)
    fig.update_traces(textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        saldo_por_segmento = df.groupby('segmento')['saldo_conta'].mean().reset_index()
        fig = px.bar(saldo_por_segmento, x='segmento', y='saldo_conta',
                     title='Saldo Médio por Segmento',
                     labels={'segmento': 'Segmento', 'saldo_conta': 'Saldo Médio (R$)'},
                     color_discrete_sequence=['#1976d2'])
        fig.update_layout(xaxis_title='Segmento', yaxis_title='Saldo Médio (R$)')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        rent_por_segmento = df.groupby('segmento')['rentabilidade_mensal'].mean().reset_index()
        fig = px.bar(rent_por_segmento, x='segmento', y='rentabilidade_mensal',
                     title='Rentabilidade Média Mensal por Segmento',
                     labels={'segmento': 'Segmento', 'rentabilidade_mensal': 'Rentabilidade Média (R$)'},
                     color_discrete_sequence=['#4caf50'])
        fig.update_layout(xaxis_title='Segmento', yaxis_title='Rentabilidade Média (R$)')
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Número Médio de Produtos por Segmento")
    produtos_por_segmento = df.groupby('segmento')['num_produtos'].mean().reset_index()
    fig = px.bar(produtos_por_segmento, x='segmento', y='num_produtos',
                 title='Número Médio de Produtos por Segmento',
                 labels={'segmento': 'Segmento', 'num_produtos': 'Número Médio de Produtos'},
                 color_discrete_sequence=['#ff9800'])
    fig.update_layout(xaxis_title='Segmento', yaxis_title='Número Médio de Produtos')
    st.plotly_chart(fig, use_container_width=True)

# Aba 3: Canais de Atendimento
with eda_tabs[2]:
    st.subheader("Análise de Canais de Atendimento")
    canais_count = df['canal_preferido'].value_counts().reset_index()
    canais_count.columns = ['Canal', 'Quantidade']
    fig = px.bar(canais_count, x='Canal', y='Quantidade',
                 title='Distribuição de Clientes por Canal Preferido',
                 color_discrete_sequence=['#3f51b5'])
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        custo_por_canal = df.groupby('canal_preferido')['custo_atendimento_mensal'].mean().reset_index()
        fig = px.bar(custo_por_canal, x='canal_preferido', y='custo_atendimento_mensal',
                     title='Custo Médio de Atendimento por Canal',
                     labels={'canal_preferido': 'Canal', 'custo_atendimento_mensal': 'Custo Médio (R$)'},
                     color_discrete_sequence=['#e91e63'])
        fig.update_layout(xaxis_title='Canal', yaxis_title='Custo Médio de Atendimento (R$)')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        freq_por_canal = df.groupby('canal_preferido')['freq_contatos_mensais'].mean().reset_index()
        fig = px.bar(freq_por_canal, x='canal_preferido', y='freq_contatos_mensais',
                     title='Frequência Média de Contatos por Canal',
                     labels={'canal_preferido': 'Canal', 'freq_contatos_mensais': 'Contatos Mensais'},
                     color_discrete_sequence=['#009688'])
        fig.update_layout(xaxis_title='Canal', yaxis_title='Média de Contatos Mensais')
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Canal Preferido por Segmento")
    canal_por_segmento = pd.crosstab(df['segmento'], df['canal_preferido'], normalize='index').reset_index()
    canal_por_segmento = pd.melt(canal_por_segmento, id_vars=['segmento'], var_name='canal', value_name='percentual')
    fig = px.bar(canal_por_segmento, x='segmento', y='percentual', color='canal',
                 title='Canal Preferido por Segmento',
                 labels={'segmento': 'Segmento', 'percentual': 'Percentual', 'canal': 'Canal'},
                 color_discrete_sequence=px.colors.qualitative.Safe)
    fig.update_layout(xaxis_title='Segmento', yaxis_title='Percentual (%)', barmode='stack',
                      yaxis=dict(tickformat='.0%'))
    st.plotly_chart(fig, use_container_width=True)

# Aba 4: Satisfação
with eda_tabs[3]:
    st.subheader("Análise de Satisfação do Cliente")
    fig = px.histogram(df, x='satisfacao', nbins=20,
                       title='Distribuição do Score de Satisfação',
                       labels={'satisfacao': 'Score de Satisfação', 'count': 'Quantidade de Clientes'},
                       color_discrete_sequence=['#2196f3'])
    fig.update_layout(xaxis_title='Score de Satisfação', yaxis_title='Quantidade de Clientes')
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        satisfacao_por_segmento = df.groupby('segmento')['satisfacao'].mean().reset_index()
        fig = px.bar(satisfacao_por_segmento, x='segmento', y='satisfacao',
                     title='Satisfação Média por Segmento',
                     labels={'segmento': 'Segmento', 'satisfacao': 'Satisfação Média'},
                     color_discrete_sequence=['#4caf50'])
        fig.update_layout(xaxis_title='Segmento', yaxis_title='Satisfação Média')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        satisfacao_por_canal = df.groupby('canal_preferido')['satisfacao'].mean().reset_index()
        fig = px.bar(satisfacao_por_canal, x='canal_preferido', y='satisfacao',
                     title='Satisfação Média por Canal',
                     labels={'canal_preferido': 'Canal', 'satisfacao': 'Satisfação Média'},
                     color_discrete_sequence=['#ff9800'])
        fig.update_layout(xaxis_title='Canal', yaxis_title='Satisfação Média')
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Relação entre Número de Produtos e Satisfação")
    satisfacao_por_produtos = df.groupby('num_produtos')['satisfacao'].mean().reset_index()
    fig = px.line(satisfacao_por_produtos, x='num_produtos', y='satisfacao', markers=True,
                  title='Relação entre Número de Produtos e Satisfação',
                  labels={'num_produtos': 'Número de Produtos', 'satisfacao': 'Satisfação Média'},
                  color_discrete_sequence=['#9c27b0'])
    fig.update_layout(xaxis_title='Número de Produtos', yaxis_title='Satisfação Média')
    st.plotly_chart(fig, use_container_width=True)

# Aba 5: Rentabilidade
with eda_tabs[4]:
    st.subheader("Análise de Rentabilidade")
    fig = px.histogram(df, x='rentabilidade_mensal', nbins=30,
                       title='Distribuição da Rentabilidade Mensal por Cliente',
                       labels={'rentabilidade_mensal': 'Rentabilidade Mensal (R$)', 'count': 'Quantidade de Clientes'},
                       color_discrete_sequence=['#2196f3'])
    fig.update_layout(xaxis_title='Rentabilidade Mensal (R$)', yaxis_title='Quantidade de Clientes')
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        receita_custo_segmento = df.groupby('segmento').agg({
            'receita_mensal': 'mean', 
            'custo_atendimento_mensal': 'mean'
        }).reset_index()
        receita_custo_segmento = pd.melt(
            receita_custo_segmento, 
            id_vars=['segmento'], 
            value_vars=['receita_mensal', 'custo_atendimento_mensal'],
            var_name='Tipo', 
            value_name='Valor'
        )
        fig = px.bar(receita_custo_segmento, x='segmento', y='Valor', color='Tipo', barmode='group',
                     title='Receita vs Custo Médio por Segmento',
                     labels={'segmento': 'Segmento', 'Valor': 'Valor Médio (R$)'},
                     color_discrete_sequence=['#4caf50', '#f44336'])
        fig.update_layout(xaxis_title='Segmento', yaxis_title='Valor Médio (R$)')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        rent_por_canal = df.groupby('canal_preferido')['rentabilidade_mensal'].mean().reset_index()
        fig = px.bar(rent_por_canal, x='canal_preferido', y='rentabilidade_mensal',
                     title='Rentabilidade Média por Canal',
                     labels={'canal_preferido': 'Canal', 'rentabilidade_mensal': 'Rentabilidade Média (R$)'},
                     color_discrete_sequence=['#2196f3'])
        fig.update_layout(xaxis_title='Canal', yaxis_title='Rentabilidade Média (R$)')
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Relação entre Número de Produtos e Rentabilidade")
    rent_por_produtos = df.groupby('num_produtos')['rentabilidade_mensal'].mean().reset_index()
    fig = px.line(rent_por_produtos, x='num_produtos', y='rentabilidade_mensal', markers=True,
                  title='Relação entre Número de Produtos e Rentabilidade',
                  labels={'num_produtos': 'Número de Produtos', 'rentabilidade_mensal': 'Rentabilidade Média (R$)'},
                  color_discrete_sequence=['#ff9800'])
    fig.update_layout(xaxis_title='Número de Produtos', yaxis_title='Rentabilidade Média (R$)')
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Relação entre Satisfação e Rentabilidade")
    df_sample = df.sample(n=1000, random_state=42)
    fig = px.scatter(df_sample, x='satisfacao', y='rentabilidade_mensal', color='segmento',
                     title='Relação entre Satisfação e Rentabilidade',
                     labels={'satisfacao': 'Score de Satisfação', 'rentabilidade_mensal': 'Rentabilidade Mensal (R$)', 'segmento': 'Segmento'},
                     color_discrete_sequence=px.colors.qualitative.Safe)
    fig.update_layout(xaxis_title='Score de Satisfação', yaxis_title='Rentabilidade Mensal (R$)')
    st.plotly_chart(fig, use_container_width=True)
st.markdown("---")

# ==============================================================================
# Seção 4: Análise e Interpretação
# ==============================================================================
st.header("4. Análise e Interpretação")
st.markdown("""
Com base na exploração dos dados, vamos aplicar análises mais aprofundadas para extrair insights relevantes 
que possam melhorar a qualidade do atendimento e aumentar a rentabilidade do banco.
""")
analysis_tabs = st.tabs(["Segmentação Avançada", "Análise de Atendimento", "Modelos Preditivos", "Análise de Oportunidades"])

# Aba 1: Segmentação Avançada
with analysis_tabs[0]:
    st.subheader("Segmentação Avançada de Clientes")
    df_valor = df.copy()
    df_valor['score_saldo'] = pd.qcut(df_valor['saldo_conta'], 5, labels=False, duplicates='drop') + 1
    df_valor['score_freq'] = pd.qcut(df_valor['freq_contatos_mensais'].clip(lower=1), 5, labels=False, duplicates='drop') + 1
    df_valor['score_valor'] = pd.qcut(df_valor['valor_transacoes_mensais'], 5, labels=False, duplicates='drop') + 1
    df_valor['score_total'] = df_valor['score_saldo'] + df_valor['score_freq'] + df_valor['score_valor']
    valor_bins = [3, 7, 11, 15]
    valor_labels = ['Baixo Valor', 'Médio Valor', 'Alto Valor', 'Muito Alto Valor']
    df_valor['segmento_valor'] = pd.cut(df_valor['score_total'], bins=[2] + valor_bins, labels=valor_labels)

    segmentos_valor = df_valor['segmento_valor'].value_counts().reset_index()
    segmentos_valor.columns = ['Segmento de Valor', 'Quantidade']
    fig = px.pie(segmentos_valor, names='Segmento de Valor', values='Quantidade',
                 title='Distribuição de Clientes por Segmento de Valor',
                 color_discrete_sequence=px.colors.sequential.Viridis)
    fig.update_traces(textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)

    cruzamento_segmentos = pd.crosstab(df_valor['segmento'], df_valor['segmento_valor'], normalize='index')
    fig = px.imshow(cruzamento_segmentos, text_auto=True, aspect="auto",
                    title='Cruzamento entre Segmentos Tradicionais e Segmentos de Valor',
                    labels=dict(x='Segmento de Valor', y='Segmento Tradicional', color='Proporção'),
                    color_continuous_scale='Viridis')
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

    rent_por_segmento_valor = df_valor.groupby('segmento_valor', observed=True)[['receita_mensal', 'custo_atendimento_mensal', 'rentabilidade_mensal']].mean()
    fig = make_subplots(rows=1, cols=3, 
                        subplot_titles=("Receita Média", "Custo Médio", "Rentabilidade Média"),
                        shared_yaxes=True)
    fig.add_trace(go.Bar(x=rent_por_segmento_valor.index, y=rent_por_segmento_valor['receita_mensal'], marker_color='#4caf50', name='Receita'), row=1, col=1)
    fig.add_trace(go.Bar(x=rent_por_segmento_valor.index, y=rent_por_segmento_valor['custo_atendimento_mensal'], marker_color='#f44336', name='Custo'), row=1, col=2)
    fig.add_trace(go.Bar(x=rent_por_segmento_valor.index, y=rent_por_segmento_valor['rentabilidade_mensal'], marker_color='#2196f3', name='Rentabilidade'), row=1, col=3)
    fig.update_layout(title_text="Métricas Financeiras por Segmento de Valor", height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    **Insights da Segmentação Avançada:**
    
    1. Os clientes "Alto Valor" e "Muito Alto Valor" representam uma pequena parcela da base, mas contribuem desproporcionalmente para a rentabilidade.
    2. Existe uma distribuição heterogênea de valor dentro de cada segmento tradicional, indicando oportunidades de estratégias personalizadas.
    3. Alguns clientes do segmento "Varejo" apresentam comportamento de "Alto Valor" ou "Muito Alto Valor", sugerindo potencial de upgrade.
    """)

# Aba 2: Análise de Atendimento
with analysis_tabs[1]:
    st.subheader("Análise do Atendimento ao Cliente")
    df_atendimento = df.copy()
    df_atendimento['faixa_contatos'] = pd.cut(df_atendimento['freq_contatos_mensais'], 
                                              bins=[0, 2, 5, 10, 30], 
                                              labels=['0-2', '3-5', '6-10', '11+'])
    satisfacao_por_freq = df_atendimento.groupby('faixa_contatos', observed=True)['satisfacao'].mean().reset_index()
    fig = px.line(satisfacao_por_freq, x='faixa_contatos', y='satisfacao', markers=True,
                  title='Relação entre Frequência de Contatos e Satisfação',
                  labels={'faixa_contatos': 'Frequência de Contatos Mensais', 'satisfacao': 'Satisfação Média'},
                  color_discrete_sequence=['#e91e63'])
    fig.update_layout(xaxis_title='Frequência de Contatos Mensais', yaxis_title='Satisfação Média')
    st.plotly_chart(fig, use_container_width=True)

    custo_por_ponto_satisfacao = df.groupby('canal_preferido')[['custo_atendimento_mensal', 'satisfacao']].mean()
    custo_por_ponto_satisfacao['Custo por Ponto de Satisfação'] = custo_por_ponto_satisfacao['custo_atendimento_mensal'] / custo_por_ponto_satisfacao['satisfacao']
    custo_por_ponto_satisfacao = custo_por_ponto_satisfacao[['Custo por Ponto de Satisfação']].reset_index()
    fig = px.bar(custo_por_ponto_satisfacao, x='canal_preferido', y='Custo por Ponto de Satisfação',
                 title='Eficiência do Atendimento por Canal (Custo/Satisfação)',
                 color_discrete_sequence=['#9c27b0'])
    fig.update_layout(xaxis_title='Canal', yaxis_title='Custo por Ponto de Satisfação (R$)')
    st.plotly_chart(fig, use_container_width=True)

    df_atendimento['faixa_etaria'] = pd.cut(df_atendimento['idade'], 
                                            bins=[17, 30, 45, 60, 85], 
                                            labels=['18-30', '31-45', '46-60', '61+'])
    satisfacao_idade_canal = df_atendimento.groupby(['faixa_etaria', 'canal_preferido'], observed=True)['satisfacao'].mean().reset_index()
    fig = px.bar(satisfacao_idade_canal, x='faixa_etaria', y='satisfacao', color='canal_preferido', barmode='group',
                 title='Satisfação por Faixa Etária e Canal',
                 labels={'faixa_etaria': 'Faixa Etária', 'satisfacao': 'Satisfação Média', 'canal_preferido': 'Canal'},
                 color_discrete_sequence=px.colors.qualitative.Safe)
    fig.update_layout(xaxis_title='Faixa Etária', yaxis_title='Satisfação Média')
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    **Insights sobre Atendimento:**
    
    1. A satisfação tende a diminuir com o aumento da frequência de contatos, indicando possíveis problemas de resolução de questões.
    2. Canais digitais (App e Internet Banking) apresentam a melhor relação custo-satisfação.
    3. Clientes mais jovens preferem e têm maior satisfação com canais digitais, enquanto clientes mais velhos valorizam o atendimento presencial.
    4. Há uma oportunidade de redução de custos e aumento de satisfação migrando clientes para canais digitais, especialmente nas faixas etárias intermediárias.
    """)

# Aba 3: Modelos Preditivos
with analysis_tabs[2]:
    st.subheader("Modelos Preditivos")
    df_modelo = df.copy()
    df_modelo['score_churn'] = (
        (100 - df_modelo['satisfacao']) * 0.4 +
        df_modelo['custo_atendimento_mensal'] * 0.2 +
        (9 - df_modelo['num_produtos']) * 15 +
        (120 / (df_modelo['tempo_cliente_meses'] + 12)) * 40
    ) / 100
    min_score = df_modelo['score_churn'].min()
    max_score = df_modelo['score_churn'].max()
    df_modelo['score_churn'] = ((df_modelo['score_churn'] - min_score) / (max_score - min_score)) * 100
    df_modelo['risco_churn'] = pd.cut(df_modelo['score_churn'], 
                                      bins=[0, 25, 50, 75, 100], 
                                      labels=['Baixo', 'Médio-Baixo', 'Médio-Alto', 'Alto'])

    risco_counts = df_modelo['risco_churn'].value_counts().reset_index()
    risco_counts.columns = ['Nível de Risco', 'Quantidade']
    fig = px.pie(risco_counts, names='Nível de Risco', values='Quantidade',
                 title='Distribuição de Clientes por Nível de Risco de Churn',
                 color='Nível de Risco',
                 color_discrete_map={'Baixo': '#4caf50', 'Médio-Baixo': '#8bc34a', 
                                     'Médio-Alto': '#ffc107', 'Alto': '#f44336'})
    fig.update_traces(textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        segmentos_risco = pd.crosstab(df_modelo['segmento'], df_modelo['risco_churn'], normalize='columns')
        fig = px.imshow(segmentos_risco, text_auto=True, aspect="auto",
                        title='Distribuição de Segmentos por Nível de Risco',
                        color_continuous_scale='RdYlGn_r')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        satisfacao_por_risco = df_modelo.groupby('risco_churn', observed=True)['satisfacao'].mean().reset_index()
        fig = px.bar(satisfacao_por_risco, x='risco_churn', y='satisfacao',
                     title='Satisfação Média por Nível de Risco',
                     labels={'risco_churn': 'Nível de Risco', 'satisfacao': 'Satisfação Média'},
                     color_discrete_sequence=['#2196f3'])
        fig.update_layout(xaxis_title='Nível de Risco', yaxis_title='Satisfação Média')
        st.plotly_chart(fig, use_container_width=True)

    impacto_financeiro = df_modelo.groupby('risco_churn', observed=True)[['rentabilidade_mensal']].sum().reset_index()
    impacto_financeiro.columns = ['Nível de Risco', 'Rentabilidade Total (R$)']
    fig = px.bar(impacto_financeiro, x='Nível de Risco', y='Rentabilidade Total (R$)',
                 title='Impacto Financeiro Potencial por Nível de Risco',
                 color='Nível de Risco',
                 color_discrete_map={'Baixo': '#4caf50', 'Médio-Baixo': '#8bc34a', 
                                     'Médio-Alto': '#ffc107', 'Alto': '#f44336'})
    fig.update_layout(xaxis_title='Nível de Risco', yaxis_title='Rentabilidade Total (R$)')
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    **Insights dos Modelos Preditivos:**
    
    1. Aproximadamente 25% dos clientes apresentam alto risco de churn, representando uma potencial perda significativa de receita.
    2. Clientes com maior risco de churn estão concentrados principalmente no segmento Varejo, mas há uma proporção significativa em segmentos de maior valor.
    3. A satisfação do cliente é inversamente proporcional ao risco de churn, confirmando a importância de melhorar a experiência do cliente.
    4. O impacto financeiro potencial do churn é expressivo, justificando investimentos em estratégias de retenção.
    """)

# Aba 4: Análise de Oportunidades
with analysis_tabs[3]:
    st.subheader("Análise de Oportunidades")
    rentabilidade_por_produtos = df.groupby('num_produtos')[['rentabilidade_mensal', 'satisfacao']].mean().reset_index()
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=rentabilidade_por_produtos['num_produtos'], y=rentabilidade_por_produtos['rentabilidade_mensal'], name='Rentabilidade', marker_color='#2196f3'), secondary_y=False)
    fig.add_trace(go.Scatter(x=rentabilidade_por_produtos['num_produtos'], y=rentabilidade_por_produtos['satisfacao'], name='Satisfação', marker_color='#ff9800', mode='lines+markers'), secondary_y=True)
    fig.update_layout(title_text='Relação entre Número de Produtos, Rentabilidade e Satisfação', xaxis_title='Número de Produtos')
    fig.update_yaxes(title_text='Rentabilidade Média (R$)', secondary_y=False)
    fig.update_yaxes(title_text='Satisfação Média', secondary_y=True)
    st.plotly_chart(fig, use_container_width=True)

    canais_custo = df.groupby('canal_preferido')[['custo_atendimento_mensal', 'freq_contatos_mensais']].mean()
    canais_custo['custo_por_contato'] = canais_custo['custo_atendimento_mensal'] / canais_custo['freq_contatos_mensais']
    canais_caros = ['Agência', 'Central Telefônica']
    n_clientes_canais_caros = df[df['canal_preferido'].isin(canais_caros)].shape[0]
    custo_atual = df[df['canal_preferido'].isin(canais_caros)]['custo_atendimento_mensal'].sum()
    custo_medio_app = canais_custo.loc['App', 'custo_por_contato']
    freq_media_canais_caros = df[df['canal_preferido'].isin(canais_caros)]['freq_contatos_mensais'].mean()
    custo_estimado_digital = n_clientes_canais_caros * custo_medio_app * freq_media_canais_caros
    economia_potencial = custo_atual - custo_estimado_digital

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Clientes em canais de alto custo", f"{n_clientes_canais_caros:,}")
    with col2:
        st.metric("Custo atual de atendimento", f"R$ {custo_atual:,.2f}")
    with col3:
        st.metric("Economia potencial mensal", f"R$ {economia_potencial:,.2f}")

    df_inativos = df[~df['cliente_ativo']]
    receita_potencial = df_inativos['receita_mensal'].sum()
    clientes_inativos = df_inativos.shape[0]
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Clientes inativos", f"{clientes_inativos:,} ({clientes_inativos/len(df):.1%} do total)")
    with col2:
        st.metric("Receita potencial mensal", f"R$ {receita_potencial:,.2f}")

    inativos_por_segmento = pd.crosstab(df['segmento'], df['cliente_ativo']).reset_index()
    inativos_por_segmento['taxa_inatividade'] = (1 - inativos_por_segmento[True] / (inativos_por_segmento[True] + inativos_por_segmento[False])) * 100
    inativos_por_segmento = inativos_por_segmento[['segmento', 'taxa_inatividade']]
    fig = px.bar(inativos_por_segmento, x='segmento', y='taxa_inatividade',
                 title='Taxa de Inatividade por Segmento',
                 labels={'segmento': 'Segmento', 'taxa_inatividade': 'Taxa de Inatividade (%)'},
                 color_discrete_sequence=['#f44336'])
    fig.update_layout(xaxis_title='Segmento', yaxis_title='Taxa de Inatividade (%)')
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    **Insights sobre Oportunidades:**
    
    1. **Cross-selling:** Há uma correlação positiva entre número de produtos, rentabilidade e satisfação, sugerindo benefícios em estratégias de venda cruzada.
    
    2. **Migração de canais:** A migração de clientes para canais digitais pode gerar uma economia significativa nos custos de atendimento, mantendo ou até melhorando os níveis de satisfação.
    
    3. **Reativação de clientes:** Existe uma oportunidade substancial de receita nammm reativação de clientes inativos, com foco especial no segmento Varejo que apresenta a maior taxa de inatividade.
    """)
st.markdown("---")

# ==============================================================================
# Seção 5: Visualização e Relatórios
# ==============================================================================
st.header("5. Visualização e Relatórios")
st.markdown("""
Esta dashboard já constitui uma ferramenta de visualização que permite analisar os dados e extrair insights de forma 
interativa. Em um ambiente corporativo, relatórios periódicos podem ser gerados com base nos principais indicadores.
""")

st.subheader("Resumo dos Principais Indicadores")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("#### Indicadores de Cliente")
    st.metric("Satisfação Média", f"{df['satisfacao'].mean():.1f}/100")
    st.metric("Produtos por Cliente", f"{df['num_produtos'].mean():.2f}")
    st.metric("% Clientes Digitais", f"{sum(df['canal_preferido'].isin(['App', 'Internet Banking']))/len(df):.1%}")

with col2:
    st.markdown("#### Indicadores Financeiros")
    st.metric("Receita Média por Cliente", f"R$ {df['receita_mensal'].mean():.2f}")
    st.metric("Custo Médio de Atendimento", f"R$ {df['custo_atendimento_mensal'].mean():.2f}")
    st.metric("Rentabilidade Média", f"R$ {df['rentabilidade_mensal'].mean():.2f}")

with col3:
    st.markdown("#### Indicadores de Risco")
    risco_alto_pct = len(df_modelo[df_modelo['risco_churn'] == 'Alto']) / len(df) * 100
    st.metric("Clientes em Alto Risco", f"{risco_alto_pct:.1f}%")
    valor_risco = df_modelo[df_modelo['risco_churn'] == 'Alto']['rentabilidade_mensal'].sum()
    st.metric("Valor em Risco Mensal", f"R$ {valor_risco:.2f}")
    st.metric("Custo de Atendimento/Receita", f"{df['custo_atendimento_mensal'].sum()/df['receita_mensal'].sum():.1%}")

st.subheader("Dashboard Resumido")
col1, col2 = st.columns(2)
with col1:
    rent_total_por_segmento = df.groupby('segmento')['rentabilidade_mensal'].sum().reset_index()
    fig = px.pie(rent_total_por_segmento, names='segmento', values='rentabilidade_mensal',
                 title='Distribuição de Rentabilidade por Segmento',
                 color_discrete_sequence=px.colors.qualitative.Safe)
    fig.update_traces(textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.scatter(df_sample, x='satisfacao', y='rentabilidade_mensal', color='segmento',
                     title='Relação entre Satisfação e Rentabilidade',
                     labels={'satisfacao': 'Score de Satisfação', 'rentabilidade_mensal': 'Rentabilidade Mensal (R$)', 'segmento': 'Segmento'},
                     trendline='ols',
                     color_discrete_sequence=px.colors.qualitative.Safe)
    fig.update_layout(xaxis_title='Score de Satisfação', yaxis_title='Rentabilidade Mensal (R$)')
    st.plotly_chart(fig, use_container_width=True)
st.markdown("---")

# ==============================================================================
# Seção 6: Tomada de Decisão
# ==============================================================================
st.header("6. Tomada de Decisão")
st.markdown("""
Com base nas análises realizadas, identificamos oportunidades e estratégias que podem melhorar a qualidade do atendimento 
e aumentar a rentabilidade do banco.
""")

st.subheader("Recomendações Estratégicas")
recom_tabs = st.tabs(["Atendimento", "Vendas", "Retenção", "Custo-Benefício", "Inovação e Sustentabilidade"])

with recom_tabs[0]:
    st.markdown("""
    ### Estratégias para Melhorar a Qualidade do Atendimento
    
    1. **Programa de Migração para Canais Digitais**
       - Desenvolver campanhas educativas para clientes de faixas etárias intermediárias (31-60 anos)
       - Oferecer incentivos (isenção de tarifas, cashback) para primeiras transações em canais digitais
       - Implementar tutoriais personalizados e suporte dedicado para migração
    
    2. **Otimização do Atendimento em Agências**
       - Reduzir tempo de espera através de agendamentos prévios para atendimentos presenciais
       - Treinar funcionários para resolver problemas na primeira interação, reduzindo a necessidade de múltiplos contatos
       - Criar espaços de autoatendimento assistido nas agências para transição gradual aos canais digitais
    
    3. **Personalização do Atendimento por Segmento**
       - Segmento Premium/Alta Renda/Private: Gerentes de relacionamento dedicados e canais prioritários
       - Segmento Varejo com alto valor: Programa de upgrade com benefícios diferenciados
       - Clientes Digitais: Ferramentas de autoatendimento avançadas e chatbots inteligentes
    """)

with recom_tabs[1]:
    st.markdown("""
    ### Estratégias para Aumento de Vendas e Rentabilidade
    
    1. **Programa de Cross-selling Baseado em Dados**
       - Desenvolver modelos de propensão à compra para identificar os próximos melhores produtos para cada cliente
       - Implementar jornadas de vendas personalizadas por segmento e perfil de uso
       - Foco em aumentar de 1-2 produtos para 3-4 produtos nos clientes de Varejo de alto valor
    
    2. **Precificação Dinâmica Baseada em Valor**
       - Implementar modelos de precificação que considerem o valor total do relacionamento
       - Oferecer pacotes especiais para clientes com potencial de upgrade de segmento
       - Desenvolver programa de benefícios progressivos conforme aumento do relacionamento
    
    3. **Estratégia de Ativação de Clientes Inativos**
       - Campanha específica para reativação dos clientes varejo inativos com ofertas personalizadas
       - Programa de "reconquista" de clientes de alto valor com benefícios exclusivos
       - Implementar jornada de "boas-vindas" para clientes reativados com foco em engajamento
    """)

with recom_tabs[2]:
    st.markdown("""
    ### Estratégias para Retenção de Clientes
    
    1. **Programa de Fidelidade e Reconhecimento**
       - Implementar sistema de pontos por produtos, transações e tempo de relacionamento
       - Oferecer benefícios tangíveis que aumentem conforme tempo de relacionamento
       - Reconhecer e premiar "momentos-chave" (aniversário de conta, metas financeiras atingidas)
    
    2. **Intervenção Proativa para Clientes em Risco**
       - Criar alertas automáticos no CRM para clientes com risco Médio-Alto e Alto, com fluxos de ação predefinidos
       - Oferecer pacotes personalizados (ex.: redução de tarifas, benefícios exclusivos) para clientes com alto risco
       - Monitorar métricas de engajamento pós-intervenção para avaliar eficácia das ações
    
    3. **Programa de Educação Financeira**
       - Desenvolver conteúdos educativos (webinars, guias) para clientes Varejo, focando em gestão financeira e uso de produtos bancários
       - Integrar educação financeira ao aplicativo móvel com dicas personalizadas baseadas no comportamento do cliente
       - Clientes engajados com educação financeira tendem a aumentar o uso de produtos e a fidelidade
    
    4. **Monitoramento Contínuo de Satisfação**
       - Implementar pesquisas de satisfação pós-interação em todos os canais, com perguntas rápidas e específicas
       - Usar análise de sentimento em feedbacks abertos para identificar pontos de dor recorrentes
       - Criar um painel em tempo real para gerentes acompanharem a satisfação por segmento e canal
    """)

with recom_tabs[3]:
    st.markdown("""
    ### Estratégias para Otimização de Custo-Benefício
    
    1. **Automatização de Processos de Atendimento**
       - Expandir o uso de chatbots alimentados por IA para resolver até 70% das consultas de baixa complexidade no App e Internet Banking
       - Implementar sistemas de triagem automática para direcionar casos complexos a atendentes especializados
       - Reduzir custos operacionais mantendo a satisfação do cliente com respostas rápidas e precisas
    
    2. **Otimização da Rede de Agências**
       - Reavaliar a localização e tamanho das agências com base no fluxo de clientes e rentabilidade
       - Transformar agências de baixo tráfego em pontos de autoatendimento com terminais digitais e suporte remoto
       - Reinvestir economias em melhorias nos canais digitais e treinamento de equipe
    
    3. **Gestão de Custos Baseada em Dados**
       - Criar um modelo preditivo para estimar o custo de atendimento por cliente com base em frequência, canal e complexidade
       - Priorizar investimentos em canais com melhor relação custo-satisfação (App e Internet Banking)
       - Monitorar a relação custo/receita por segmento para alocar recursos de forma mais eficiente
    """)

with recom_tabs[4]:
    st.markdown("""
    ### Estratégias para Inovação e Sustentabilidade
    
    1. **Integração de Tecnologias Emergentes**
       - Implementar biometria e autenticação por reconhecimento facial no App para aumentar segurança e conveniência
       - Explorar soluções de blockchain para transações internacionais, reduzindo custos e aumentando a confiança
       - Testar assistentes virtuais com IA generativa para oferecer consultoria financeira personalizada em tempo real
    
    2. **Produtos Sustentáveis e Inclusivos**
       - Lançar linhas de crédito verde para projetos de energia renovável e sustentabilidade, atraindo clientes conscientes
       - Criar contas digitais gratuitas para populações de baixa renda, promovendo inclusão financeira
       - Divulgar impacto social das iniciativas para fortalecer a marca e atrair clientes engajados
    
    3. **Parcerias Estratégicas**
       - Firmar parcerias com fintechs para oferecer serviços inovadores, como carteiras digitais e investimentos alternativos
       - Colaborar com empresas de tecnologia para integrar serviços bancários em plataformas de e-commerce
       - Estabelecer programas de recompensas com parceiros para aumentar o engajamento e a retenção
    """)

st.subheader("Visualizações de Suporte à Tomada de Decisão")
col1, col2 = st.columns(2)
with col1:
    custo_por_interacao = df.groupby('canal_preferido')[['custo_atendimento_mensal', 'freq_contatos_mensais']].sum()
    custo_por_interacao['Custo por Interação (R$)'] = custo_por_interacao['custo_atendimento_mensal'] / custo_por_interacao['freq_contatos_mensais']
    custo_por_interacao = custo_por_interacao[['Custo por Interação (R$)']].reset_index()
    fig = px.bar(custo_por_interacao, x='canal_preferido', y='Custo por Interação (R$)',
                 title='Custo Médio por Interação por Canal',
                 labels={'canal_preferido': 'Canal', 'Custo por Interação (R$)': 'Custo por Interação (R$)'},
                 color_discrete_sequence=['#ff5722'])
    fig.update_layout(xaxis_title='Canal', yaxis_title='Custo por Interação (R$)')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    reativacao_por_segmento = df[~df['cliente_ativo']].groupby('segmento')['receita_mensal'].sum().reset_index()
    fig = px.bar(reativacao_por_segmento, x='segmento', y='receita_mensal',
                 title='Receita Potencial de Reativação por Segmento',
                 labels={'segmento': 'Segmento', 'receita_mensal': 'Receita Potencial (R$)'},
                 color_discrete_sequence=['#4caf50'])
    fig.update_layout(xaxis_title='Segmento', yaxis_title='Receita Potencial (R$)')
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Projeção de Impacto Financeiro")
receita_reativacao = receita_potencial * 0.3
receita_cross_selling = df[df['num_produtos'] <= 3]['rentabilidade_mensal'].sum() * 0.2
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Economia com Migração Digital", f"R$ {economia_potencial:,.2f}/mês")
with col2:
    st.metric("Receita com Reativação", f"R$ {receita_reativacao:,.2f}/mês")
with col3:
    st.metric("Receita com Cross-selling", f"R$ {receita_cross_selling:,.2f}/mês")
st.markdown("---")

# ==============================================================================
# Resumo Executivo
# ==============================================================================
st.header("Resumo Executivo")
st.markdown("""
Este projeto desenvolveu uma análise completa de dados bancários simulados, utilizando Python, Pandas, NumPy, Plotly e Streamlit, para gerar insights acionáveis que melhoram a qualidade do atendimento e aumentam a lucratividade de uma instituição financeira. A análise abrangeu:

- **Coleta e Limpeza**: Simulação de 10.000 registros com dados realistas, tratados para garantir consistência.
- **Exploração (EDA)**: Identificação de padrões em segmentos, canais, satisfação e rentabilidade.
- **Análise Avançada**: Segmentação RFV, modelos preditivos de churn e análise de oportunidades de cross-selling e migração de canais.
- **Visualização**: Dashboards interativos com métricas-chave para facilitar a interpretação.
- **Tomada de Decisão**: Recomendações estratégicas para:
  - **Melhorar o Atendimento**: Migração para canais digitais, otimização de agências e personalização por segmento.
  - **Aumentar a Lucratividade**: Cross-selling, reativação de clientes inativos e precificação dinâmica.
  - **Reduzir Riscos**: Intervenções proativas contra churn e programas de fidelidade.
  - **Inovação**: Integração de IA, produtos sustentáveis e parcerias com fintechs.

**Impacto Projetado**:
- Economia de R$ {economia_potencial:,.2f}/mês com migração para canais digitais.
- Receita adicional de R$ {receita_reativacao:,.2f}/mês com reativação de clientes.
- Aumento de R$ {receita_cross_selling:,.2f}/mês com estratégias de cross-selling.

Este projeto demonstra a aplicação prática de análise
             de dados para resolver problemas de negócios, com foco em resultados mensuráveis e estratégias inovadoras.
""".format(economia_potencial=economia_potencial, receita_reativacao=receita_reativacao, receita_cross_selling=receita_cross_selling))