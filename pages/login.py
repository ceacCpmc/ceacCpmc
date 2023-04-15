from app2 import *
from dash import Dash, html, dcc, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
import pandas as pd
from dash.exceptions import PreventUpdate
from werkzeug.security import check_password_hash
from flask_login import login_user
import registra_logs
from threading import Thread

card_style = {
    'width': '300px',
    'min-height': '300px',
    'padding': '30px',
    'align-self': 'center'}


def renderiza(mensagem_acesso):
    if mensagem_acesso == 'erro':
        mensagem_acesso = 'Erro! Usuário ou senha inválidos.'
    if mensagem_acesso == 'OK':
        mensagem_acesso = 'Insira os dados'

    login = dbc.Card(
        [
            html.Legend('Acesso'),
            dbc.Input(id='input_cpf_acesso', placeholder='Insira o CPF do usuário', type='text',
                      style={'margin-top': '10px'}),
            dbc.Input(id='input_senha_acesso', placeholder='Insira a senha', type='password',
                      style={'margin-top': '10px'}),
            dbc.Button('Entrar', id='botao_acesso', style={'margin-top': '10px'}),
            html.Span(mensagem_acesso, style={'text-align': 'center', 'margin-top': '10px', 'color': 'red'}),
            html.Div([
                dcc.Link('Registre-se', href='/registro'),
            ], style={'padding': '20px', 'display': 'flex', 'justify-content': 'center'}),
            html.Div([
                html.Label('Ou', style={'margin-right': '5px'}),
                dcc.Link('recupere a senha', href='/recupar'),
            ], style={'padding': '5px', 'display': 'flex', 'justify-content': 'center'}),
            html.Div([
                html.Label('Feito por CEAC/CPMC', style={'margin-right': '5px', 'textAlign': 'center',
                                                         'color': 'orange', 'fontSize': 14}),
            ], style={'padding': '10px', 'display': 'flex', 'justify-content': 'center'})
        ], color="secondary", outline=True,
        style=card_style)
    return login


@app2.callback(
    Output('login-state', "data"),
    Input('botao_acesso', 'n_clicks'),
    [
        State('input_cpf_acesso', 'value'),
        State('input_senha_acesso', 'value')
    ]
)
def sucesso_acesso(n_clicks, cpf_usuario, senha_usuario):
    if n_clicks is None:
        raise PreventUpdate

    try:
        # === RETIRAR === #
        # conn = sqlite3.connect('data.sqlite')
        # engine = create_engine('sqlite:///data.sqlite')
        #
        conn = psycopg2.connect(host='ec2-3-210-173-88.compute-1.amazonaws.com', database='d15949k84tt69d',
                                user='evgdmltwwnjdfn',
                                password='f3623d6aae90a95d478cc153c816846d9d615c3ca60385e536f76e56a175dca0')

        engine = create_engine(
            'postgresql://evgdmltwwnjdfn:f3623d6aae90a95d478cc153c816846d9d615c3ca60385e536f76e56a175dca0@ec2' \
            '-3-210-173-88.compute-1.amazonaws.com:5432/d15949k84tt69d')

        db = SQLAlchemy()
        conn.cursor()
        df = pd.read_sql('select * from users', conn)
        print('Atualmente o banco tem esses usuários')
        print(df['user_name'])
        # ==================#

        print('#/#/#/')
        print(cpf_usuario)
        print('#/#/#/')

        # Quebra da segurança apenas para avançar
        # return 'Sucesso'

        #depois retirar esse trecho


        user = Users.query.filter_by(user_cpf=cpf_usuario).first()
        print(user)
        print(user.user_password)
        print(user.user_cpf)
        print(user.user_email)
        print(user.user_name)
        print(user.user_aprovado)

        a, b, c = user.user_name, user.user_cpf, user.user_email

        if user and senha_usuario is not None:
            if check_password_hash(user.user_password, senha_usuario) and user.user_aprovado == 's':
                login_user(user)
                try:
                    th_registra_logs = Thread(target=registra_logs.registrar(a, b, c))
                    th_registra_logs.start()
                except Exception as erro:
                    print(f'Erro ao registrar o log de entrada - {erro}')
                return 'Sucesso'
            else:
                return 'erro'
        else:
            return 'erro'
    except Exception as erro:
        print(f'Erro de - {erro}')
        return 'erro'
    conn.close()

