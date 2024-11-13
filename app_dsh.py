#pip install dash
#python app_dsh.py

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)
#Read-arqv CSV
tabela = pd.read_csv('Abastecimento_Caminhao.csv', delimiter=';', on_bad_lines='skip')
#Remov UnWanted-Columns
colunas_para_excluir = ["Requisição", "Hora Abast.", "Obs.", "Abast. Externo", "Combustível"]
colunas_existentes = [col for col in colunas_para_excluir if col in tabela.columns]
if colunas_existentes:
    tabela = tabela.drop(columns=colunas_existentes)
#Convt Columns t/N°
tabela['Km Rodados'] = pd.to_numeric(tabela['Km Rodados'], errors='coerce')
tabela['Litros'] = pd.to_numeric(tabela['Litros'].astype(str).str.replace(',', '').str[:-2], errors='coerce')
tabela['Vlr. Total'] = pd.to_numeric(tabela['Vlr. Total'].astype(str).str.replace(',', ''), errors='coerce')
tabela['Horim. Equip.'] = pd.to_numeric(tabela['Horim. Equip.'], errors='coerce')
#Calc Additnl Columns
tabela['Km por Litro'] = tabela['Km Rodados'] / tabela['Litros']
tabela['Lucro'] = tabela['Km Rodados'] - tabela['Vlr. Total']
tabela['Horim por Litro'] = tabela['Horim. Equip.'] / tabela['Litros']
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
#Layout-Dash
app.layout = html.Div([
    dcc.Input(id='input-requisitante', type='text', value='GESSE', placeholder='Requisitante'),
    dcc.Input(id='input-veiculo', type='text', value='BT220', placeholder='Veículo'),
    dcc.Input(id='input-data-inicial', type='text', value='01/04/2024', placeholder='Data Inicial (DD/MM/AAAA)'),
    dcc.Input(id='input-data-final', type='text', value='31/07/2024', placeholder='Data Final (DD/MM/AAAA)'),
    dcc.Dropdown(
        id='analise-dropdown',
        options=[
            {'label': 'Análise 1: Km Rodados', 'value': 'analise1'},
            {'label': 'Análise 2: Litros', 'value': 'analise2'},
            {'label': 'Análise 3: Km por Litro', 'value': 'analise3'},
            {'label': 'Análise 4: Lucro', 'value': 'analise4'},
            {'label': 'Análise 5: Horim por Litro', 'value': 'analise5'}
        ],
        value='analise1'
    ),
    dcc.Graph(id='grafico')
])
@app.callback(
    Output('grafico', 'figure'),
    [Input('input-requisitante', 'value'),
     Input('input-veiculo', 'value'),
     Input('input-data-inicial', 'value'),
     Input('input-data-final', 'value'),
     Input('analise-dropdown', 'value')]
)
def update_graph(requisitante, veiculo, data_inicial, data_final, analise):
    tabela['Data Req.'] = pd.to_datetime(tabela['Data Req.'], format='%d/%m/%Y')
    data_inicial = pd.to_datetime(data_inicial, format='%d/%m/%Y')
    data_final = pd.to_datetime(data_final, format='%d/%m/%Y')
    filtro = tabela[(tabela['Requisitante'].str.contains(requisitante, case=False, na=False)) &
                    (tabela['Veículo/Equip.'].str.contains(veiculo, case=False, na=False)) &
                    (tabela['Data Req.'] >= data_inicial) &
                    (tabela['Data Req.'] <= data_final)]

    if analise == 'analise1':
        fig = analise1(filtro)
    elif analise == 'analise2':
        fig = analise2(filtro)
    elif analise == 'analise3':
        fig = analise3(filtro)
    elif analise == 'analise4':
        fig = analise4(filtro)
    elif analise == 'analise5':
        fig = analise5(filtro)

    return fig
if __name__ == '__main__':
    app.run_server(debug=True)