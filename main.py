import dash
from dash import html, dcc
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
from pandas.api.types import is_numeric_dtype
import plotly.express as px
import plotly.graph_objects as go
import os
import pickle
from log_estate import meuLog, inicializaLog


# ---- setup ---- #
pathApp = './'
s1, s2, s3 = 0, 0, 0

# ---- modelos ---- #
try:
    with open(f'{pathApp}data/vAluguel.pkl', 'rb') as f:
        modeloAluguel = pickle.load(f)
        meuLog("info", "modelo aluguel carregado")
except:
    meuLog("warning", "modelo inexistente")


try:
    with open(f'{pathApp}data/vCondominio.pkl', 'rb') as f:
        modeloCondominio = pickle.load(f)
        meuLog("info", "modelo condominio carregado")
except:
    meuLog("warning", "modelo inexistente")


try:
    with open(f'{pathApp}data/vIptu.pkl', 'rb') as f:
        modeloIptu = pickle.load(f)
        meuLog("info", "modelo iptu carregado")
except:
    meuLog("warning", "modelo inexistente")

# ---- data ---- #
try:
    dados = pd.read_csv(f'{pathApp}data/vDados.csv')
    def getCol(col):
        teste = dados[dados[col] != -1][col].sort_values().unique().tolist()
        lista = []
        for t in range(0, len(teste)):
            dic = {}
            dic['label'] = str(teste[t])
            if is_numeric_dtype(dados[col]):
                dic['value'] = teste[t]
            else:
                dic['value'] = t
            lista.append(dic)
        # print(lista)
        return lista
    meuLog("info", "dados carregados")
except:
    meuLog("warning", "dados inacessíveis")

# --- layout app ---#
meuLog(MSG="Montando o layout")
elementos = [
    # HEADER
    dbc.Row([    
        dbc.Col([
            html.Img(src='/assets/logo.jpeg',style={'width': '80%'})
        ], width=2),    
        dbc.Col([ 
            html.Br(),           
            html.H1("AI Predictions - empower your dreams!")
        ], width=10)
    ], justify='around'),
    # FORMULARIO
    dbc.Row([
        dbc.Col([
            html.B("Looking For"),
            dcc.Dropdown(options=getCol('finalidade'), value=0, id='id-finalidade')
        ], width=5, lg=2), 
        
        dbc.Col([
            html.B("City"),
            dcc.Dropdown(getCol('cidade'), value=0, id='id-cidade')
        ], width=5, lg=2),
        dbc.Col([
            html.B("Local"),
            dcc.Dropdown(getCol('bairro'), value=5, id='id-bairro')
        ], width=5, lg=2),
        dbc.Col([
            html.B("Type"),
            dcc.Dropdown(getCol('tipo'), value=0, id='id-tipo')
        ], width=4, lg=2), 
         
    # ], justify='left'),

    # dbc.Row([
        dbc.Col([
            html.B("Beds"),
            dcc.Dropdown(getCol('quarto'), 3, id='id-quarto')
        ], width=3, lg=1), 
        dbc.Col([
            html.B("Baths"),
            dcc.Dropdown(getCol('banheiro'), 2, id='id-banheiro')
        ], width=3, lg=1), 
        dbc.Col([
            html.B("Garage"),
            dcc.Dropdown(getCol('vaga'), 2, id='id-garagem')
        ], width=3, lg=1), 
        dbc.Col([
            html.B("Feet"),
            dcc.Input(id='id-mt2', placeholder="45.12", type="text", value=100, size="2")
        ], width=1, lg=1), 
        

    ], justify='left'),

    # FILTRO
    dbc.Row([
        dbc.Col([html.Br(),html.Div("Key's value:"),html.Div(id='od-finalidade')], width=10),
        
    ], justify='left'),
    dbc.Row([
        dbc.Col([html.Br(),html.Br(),html.Div(id='resultado')], width=5),
    ], justify='left'),

    # PREVISAO

    
    dbc.Row([
        # total
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    dbc.Col([
                        html.H3('Total $'),
                        html.H1('R$ 0.0', id='id_total')
                    ])
                ]), color = 'lightgreen'                
            )
        ], width=9, lg=3),
        
    # ], justify="center"),
    
    # aluguel
    # dbc.Row([ html.Br() ], justify="center"),
    # dbc.Row([
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    dbc.Col([
                        html.H3('Rent'),
                        html.H1('R$ 0', id='id_totAluguel')
                    ])
                ]), color = 'lightblue'                
            )
        ], width=9, lg=3),

        
        
        
    # ], justify="center"),
    
    # dbc.Row([ html.Br() ], justify="center"),
    # condominio
    # dbc.Row([
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    dbc.Col([
                        html.H3('Condominium '),
                        html.H1('R$ 0', id='id_totCondominio')
                    ])
                ]), color = 'lightblue'                
            ),
            
        ], width=9, lg=3),
        
        
    # ], justify="center"),

    # dbc.Row([ html.Br() ], justify="center"),
    # IPTU
    # dbc.Row([
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    dbc.Col([
                        html.H3('Tax'),
                        html.H1('R$ 0', id='id_totIptu')
                    ])
                ]), color = 'lightblue'                
            )
        ], width=9, lg=3),
        
        
    ], justify="center"),

    dbc.Row([ html.Br() ], justify="center"),    
    
]

meuLog(MSG="Criando Dash DBC")
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}])
server = app.server
app.layout = dbc.Container(
    elementos
)

# ---- callbacks ---- #
# filtro
@app.callback(
    Output('od-finalidade', 'children'),
    Input('id-finalidade', 'value'),
    Input('id-cidade', 'value'),
    Input('id-tipo', 'value'),
    Input('id-bairro', 'value'),
    Input('id-quarto', 'value'),
    Input('id-banheiro', 'value'),
    Input('id-garagem', 'value'),
    Input('id-mt2', 'value'),
)
def atualiza_filtro(finalidade, cidade, tipo, bairro, quarto, banheiro, vaga, mt2):
    meuLog(MSG=f"Filtro: {finalidade} | {cidade} | {tipo} | {bairro} | {quarto} | {banheiro} | {vaga} | {mt2}")
    return f"{finalidade} | {cidade} | {tipo} | {bairro} | {quarto} | {banheiro} | {vaga} | {mt2}"

# previsão aluguel
@app.callback(
    Output('id_totAluguel', 'children'),
    Input('id-finalidade', 'value'),
    Input('id-cidade', 'value'),
    Input('id-tipo', 'value'),
    Input('id-bairro', 'value'),
    Input('id-quarto', 'value'),
    Input('id-banheiro', 'value'),
    Input('id-garagem', 'value'),
    Input('id-mt2', 'value'),
)
def update_previsao(finalidade,cidade,tipo,bairro,quarto,banheiro, garagem,mt2):
    dic = {
        'tipo_id': tipo,        
        'bairro_id': bairro,
        'cidade_id': cidade,
        'quarto': quarto,
        'banheiro': banheiro, 
        'vaga': garagem, 
        'mt2': mt2,
        'finalidade_id': finalidade
    }
    try:
        setup = pd.DataFrame([dic])
        prev = modeloAluguel.predict(setup)
        global s1
        s1 = prev[0]
        meuLog(f"Previsão do aluguel {prev[0]}")
        return f"R$ {prev[0]}"
    except:
        return 0


# previsão condominio
@app.callback(
    Output('id_totCondominio', 'children'),
    Input('id-finalidade', 'value'),
    Input('id-cidade', 'value'),
    Input('id-tipo', 'value'),
    Input('id-bairro', 'value'),
    Input('id-quarto', 'value'),
    Input('id-banheiro', 'value'),
    Input('id-garagem', 'value'),
    Input('id-mt2', 'value'),
)
def update_prev_condominio(finalidade,cidade,tipo,bairro,quarto,banheiro, garagem,mt2):
    dic = {
        'tipo_id': tipo,        
        'bairro_id': bairro,
        'cidade_id': cidade,
        'quarto': quarto,
        'banheiro': banheiro, 
        'vaga': garagem, 
        'mt2': mt2,
        'finalidade_id': finalidade
    }
    try:
        setup = pd.DataFrame([dic])
        prev = modeloCondominio.predict(setup)
        global s2
        s2 = prev[0]
        meuLog(f"Previsão do condomínio {prev[0]}")
        return f"R$ {prev[0]}"
    except:
        return 0
    

# previsão iptu
@app.callback(
    Output('id_totIptu', 'children'),
    Output('id_total', 'children'),
    Input('id-finalidade', 'value'),
    Input('id-cidade', 'value'),
    Input('id-tipo', 'value'),
    Input('id-bairro', 'value'),
    Input('id-quarto', 'value'),
    Input('id-banheiro', 'value'),
    Input('id-garagem', 'value'),
    Input('id-mt2', 'value'),
)
def update_prev_iptu(finalidade,cidade,tipo,bairro,quarto,banheiro, garagem,mt2):
    dic = {
        'tipo_id': tipo,        
        'bairro_id': bairro,
        'cidade_id': cidade,
        'quarto': quarto,
        'banheiro': banheiro, 
        'vaga': garagem, 
        'mt2': mt2,
        'finalidade_id': finalidade
    }
    try:
        setup = pd.DataFrame([dic])
        # print(setup)
        prev = modeloIptu.predict(setup)
        s3 = prev[0]
        meuLog(f"Previsão do IPTU {prev[0]}")
        meuLog(f"Previsão Total do valor {s1+s2+s3}")
        # print(s1+s2+s3)
        return f"R$ {prev[0]}", f"R$ {s1+s2+s3}"
    except:
        return 0, 0


if __name__ == '__main__':
    os.system('cls')
    inicializaLog()
    app.run_server(debug=False, port=8080)
    # app.run(debug=True, port=os.getenv("PORT", default=5000))
    # app.run_server(port=3030)
