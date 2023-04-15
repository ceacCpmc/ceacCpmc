from app2 import *
from dash import Dash, html, dcc, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
import pandas as pd
from dash.exceptions import PreventUpdate
from werkzeug.security import generate_password_hash
import pygsheets
import datetime


card_style = {
    'width': '300px',
    'min-height': '300px',
    'padding': '30px',
    'align-self': 'center', }


def renderiza(mensagem_estado_registro):
    msg_style = {'text-align': 'center', 'margin-top': '10px', 'color': 'red'}

    if mensagem_estado_registro == 'error_cadastro':
        mensagem_estado_registro = 'Erro! Problemas durante o registro.'

    if mensagem_estado_registro == 'error_senhas':
        mensagem_estado_registro = 'Erro!. As senhas precisam ser iguais.'

    if mensagem_estado_registro == 'Erro de cpf ou email':
        mensagem_estado_registro = 'Erro! Cpf e/ou emails já cadastrados anteriormente.\n' \
                                   'Mantenha contato com o CEAC/CPMC.'

    if mensagem_estado_registro == 'OK':
        mensagem_estado_registro = 'Cadastro enviado com sucesso. Aguarde aprovação.'
        msg_style = {'text-align': 'center', 'margin-top': '10px', 'color': 'green'}

    print(mensagem_estado_registro)

    registro = dbc.Card(
        [
            html.Legend('Solicitação de acesso'),
            dbc.Input(id='input_registro_usuario', placeholder='Insira o nome do usuário', type='text',
                      style={'margin-top': '10px'}),
            dbc.Input(id='input_registro_cpf', placeholder='Insira o CPF do usuário', type='text',
                      style={'margin-top': '10px'}),
            dbc.Input(id='input_registro_senha', placeholder='Insira uma senha', type='password',
                      style={'margin-top': '10px'}),
            dbc.Input(id='input_registro_senha_repetida', placeholder='Repita a mesma senha', type='password',
                      style={'margin-top': '10px'}),
            dbc.Input(id='input_registro_email', placeholder='Insira um e-mail válido', type='email',
                      style={'margin-top': '10px'}),
            dbc.Button('Registrar', id='botao_registro', style={'margin-top': '10px'}),
            html.Span(mensagem_estado_registro, style=msg_style),
            html.Div([
                html.Label('Ou', style={'margin-right': '5px'}),
                dcc.Link('Faça login', href='/login')
            ], style={'padding': '20px', 'display': 'flex', 'justify-content': 'center'})
        ], color="secondary", outline=True,
        style=card_style)
    return registro


@app2.callback(
    Output('registro-state', 'data'),
    Input('botao_registro', 'n_clicks'),
    [
        State('input_registro_usuario', 'value'),
        State('input_registro_cpf', 'value'),
        State('input_registro_senha', 'value'),
        State('input_registro_senha_repetida', 'value'),
        State('input_registro_email', 'value'),
    ]
)
def registrar(n_clicks, user_name, user_cpf, user_password, user_password_repetido, user_email):
    if n_clicks is None:
        raise PreventUpdate

    if user_password == user_password_repetido:
        if user_name is not None and user_password is not None and user_email is not None:
            try:
                hashed_password = generate_password_hash(user_password, method='sha256')
                ins = User_table.insert().values(user_cpf=user_cpf,
                                                 user_name=user_name,
                                                 user_password=hashed_password,
                                                 user_email=user_email)
                conn = engine.connect()
                try:
                    conn.execute(ins)
                except Exception as erro:
                    print(f'Erro de inserção no SQL - {erro}')
                    if 'UNIQUE' in str(erro.__context__):
                        print('Duplicação em dado exclusivo (CPF ou Email)')
                    return 'Erro de cpf ou email'
                df = pd.read_sql('select * from users', conn)
                print(df)
            except Exception as erro:
                print(f'O erro detectado foi - {erro}')

            dt_agora = datetime.datetime.utcnow() + datetime.timedelta(hours=-3)
            agora = dt_agora.strftime('%d/%m/%Y - %H:%M:%S')

            dados = [user_cpf, user_name, hashed_password, user_email, agora]
            client = pygsheets.authorize(
                client_secret='client_secret_640793899938-gmj6mrgve57e9m79ir5i5tp258dsl9kt.'
                              'apps.googleusercontent.com.json')
            sh = client.open('Python_projetos')
            wks = sh.worksheet('title', '22 - Usuarios')
            wks.add_rows(1)
            linhas = len(wks.get_col(1))
            wks.update_row(linhas, dados)
            print('Incluiu novo usuário')
            return 'OK'
        else:
            print('Deu erro')
            return 'error_cadastro'
    else:
        print('Deu erro')
        return 'error_senhas'
    conn.close()
