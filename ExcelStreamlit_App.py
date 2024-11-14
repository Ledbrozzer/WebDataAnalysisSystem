#pip install streamlit
#streamlit run ExcelStreamlit_App.py
# $ streamlit run yourscript.py

import streamlit as st
import pandas as pd
import plotly.express as px

# Ler o arquivo CSV
tabela = pd.read_csv('Abastecimento_Caminhao.csv', delimiter=';', on_bad_lines='skip')

# Remover colunas indesejadas
colunas_para_excluir = ["Requisição", "Hora Abast.", "Obs.", "Abast. Externo", "Combustível"]
colunas_existentes = [col for col in colunas_para_excluir if col in tabela.columns]
if colunas_existentes:
    tabela = tabela.drop(columns=colunas_existentes)

# Converter colunas para numérico
tabela['Km Rodados'] = pd.to_numeric(tabela['Km Rodados'], errors='coerce')
tabela['Litros'] = pd.to_numeric(tabela['Litros'].astype(str).str.replace(',', '').str[:-2], errors='coerce')
tabela['Vlr. Total'] = pd.to_numeric(tabela['Vlr. Total'].astype(str).str.replace(',', ''), errors='coerce')
tabela['Horim. Equip'] = pd.to_numeric(tabela['Horim. Equip.'], errors='coerce')

# Calcular colunas adicionais
tabela['Km por Litro'] = tabela['Km Rodados'] / tabela['Litros']
tabela['Lucro'] = tabela['Km Rodados'] - tabela['Vlr. Total']
tabela['Horim por Litro'] = tabela['Horim. Equip'] / tabela['Litros']

# Entrada do usuário
st.sidebar.header('Filtrar os Dados')
requisitante = st.sidebar.text_input('Requisitante', 'GESSE')
veiculo = st.sidebar.text_input('Veículo', 'BT220')
data_inicial = st.sidebar.date_input('Data inicial', pd.to_datetime('2024-04-01'))
data_final = st.sidebar.date_input('Data final', pd.to_datetime('2024-07-31'))

# Filtrar os dados
tabela['Data Req.'] = pd.to_datetime(tabela['Data Req.'], format='%d/%m/%Y')
filtro = tabela[(tabela['Requisitante'].str.contains(requisitante, case=False, na=False)) &
                (tabela['Veículo/Equip.'].str.contains(veiculo, case=False, na=False)) &
                (tabela['Data Req.'] >= pd.to_datetime(data_inicial)) &
                (tabela['Data Req.'] <= pd.to_datetime(data_final))]

# Mostrar os dados filtrados
st.write("Dados Filtrados:")
st.write(filtro)

# Seleção de Análise
analise = st.sidebar.selectbox(
    'Selecione a Análise',
    ('Análise 1: Km Rodados', 'Análise 2: Litros', 'Análise 3: Km por Litro', 'Análise 4: Lucro', 'Análise 5: Horim por Litro')
)

# Funções de análise
def analise1(filtro):
    fig = px.histogram(filtro, x='Km Rodados', color='Km Rodados', title='Análise 1: Km Rodados')
    return fig

def analise2(filtro):
    fig = px.histogram(filtro, x='Litros', color='Km Rodados', title='Análise 2: Litros')
    return fig

def analise3(filtro):
    fig = px.histogram(filtro, x='Km por Litro', color='Km Rodados', title='Análise 3: Km por Litro')
    return fig

def analise4(filtro):
    fig = px.histogram(filtro, x='Lucro', color='Km Rodados', title='Análise 4: Lucro')
    return fig

def analise5(filtro):
    fig = px.histogram(filtro, x='Horim por Litro', color='Km Rodados', title='Análise 5: Horim por Litro')
    return fig

# Gerar o gráfico baseado na seleção do usuário
if analise == 'Análise 1: Km Rodados':
    fig = analise1(filtro)
elif analise == 'Análise 2: Litros':
    fig = analise2(filtro)
elif analise == 'Análise 3: Km por Litro':
    fig = analise3(filtro)
elif analise == 'Análise 4: Lucro':
    fig = analise4(filtro)
elif analise == 'Análise 5: Horim por Litro':
    fig = analise5(filtro)

# Mostrar o gráfico
st.plotly_chart(fig)

# Botão para exportar os dados filtrados
if st.button('Exportar Dados Filtrados'):
    filtro.to_csv('dados_filtrados.csv', index=False)
    st.write('Dados exportados com sucesso!')

# Link para baixar o arquivo CSV
with open('dados_filtrados.csv', 'rb') as f:
    st.download_button('Download Dados Filtrados', f, 'dados_filtrados.csv')
