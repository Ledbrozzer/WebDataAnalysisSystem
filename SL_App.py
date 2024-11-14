#pip install streamlit
#pip install openpyxl
#streamlit run SL_App.py
# $ streamlit run yourscript.py

import streamlit as st
import pandas as pd
import plotly.express as px
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
#Read-arqv CSV
tabela = pd.read_csv('Abastecimento_Caminhao.csv', delimiter=';', on_bad_lines='skip')
#Remv UnWanted Columns
colunas_para_excluir = ["Requisição", "Hora Abast.", "Obs.", "Abast. Externo", "Combustível", "Vlr. Unitário"]
colunas_existentes = [col for col in colunas_para_excluir if col in tabela.columns]
if colunas_existentes:
    tabela = tabela.drop(columns=colunas_existentes)
#Convt Columns t-N°
tabela['Km Rodados'] = pd.to_numeric(tabela['Km Rodados'], errors='coerce')
tabela['Litros'] = pd.to_numeric(tabela['Litros'].astype(str).str.replace(',', '').str[:-2], errors='coerce')
tabela['Vlr. Total'] = pd.to_numeric(tabela['Vlr. Total'].astype(str).str.replace(',', ''), errors='coerce')
tabela['Horim. Equip'] = pd.to_numeric(tabela['Horim. Equip.'], errors='coerce')
#Calc Additionl Columns
tabela['Km por Litro'] = tabela['Km Rodados'] / tabela['Litros']
tabela['Lucro'] = tabela['Km Rodados'] - tabela['Vlr. Total']
tabela['Horim por Litro'] = tabela['Horim. Equip'] / tabela['Litros']
#User's Entry
st.sidebar.header('Filtrar os Dados')
requisitante = st.sidebar.text_input('Requisitante', 'GESSE')
veiculo = st.sidebar.text_input('Veículo', 'BT220')
data_inicial = st.sidebar.date_input('Data inicial', pd.to_datetime('2024-04-01'))
data_final = st.sidebar.date_input('Data final', pd.to_datetime('2024-07-31'))
#Filtr Data
tabela['Data Req.'] = pd.to_datetime(tabela['Data Req.'], format='%d/%m/%Y')
filtro = tabela[(tabela['Requisitante'].str.contains(requisitante, case=False, na=False)) &
                (tabela['Veículo/Equip.'].str.contains(veiculo, case=False, na=False)) &
                (tabela['Data Req.'] >= pd.to_datetime(data_inicial)) &
                (tabela['Data Req.'] <= pd.to_datetime(data_final))]
#Show t-filtrd Data
st.write("Dados Filtrados:")
st.write(filtro)
#Analysis'Selection
analise = st.sidebar.selectbox(
    'Selecione a Análise',
    ('Análise 1: Km Rodados', 'Análise 2: Litros', 'Análise 3: Km por Litro', 'Análise 4: Lucro', 'Análise 5: Horim por Litro')
)
#Analysis'Functions
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
#Mk Grafc-Selectd
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
#Show gráfc
st.plotly_chart(fig)
#Button-Extract t/Excel
if st.button('Exportar Dados Filtrados para Excel'):
    with pd.ExcelWriter('dados_filtrados.xlsx', engine='openpyxl') as writer:
        filtro.to_excel(writer, index=False, sheet_name='Dados Filtrados')
    st.write('Dados exportados para Excel com sucesso!')
#Link Download-arqv Excel
with open('dados_filtrados.xlsx', 'rb') as f:
    st.download_button('Baixar Dados Filtrados', f, file_name='dados_filtrados.xlsx')