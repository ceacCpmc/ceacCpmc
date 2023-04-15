import app2
from app2 import *
import pygsheets

from dash import Dash, html, dcc, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
from werkzeug.security import generate_password_hash
import datetime


card_style = {
    'width': '300px',
    'min-height': '300px',
    'padding': '30px',
    'align-self': 'center'}


def renderiza(mensagem_acesso):
    msg_style = {'text-align': 'center', 'margin-top': '10px', 'color': 'green'}

    if mensagem_acesso == 'Sucesso na mudança da senha':
        mensagem_acesso = 'Senha alterada com sucesso. Faça o login'
        msg_style = {'text-align': 'center', 'margin-top': '10px', 'color': 'green'}

    if mensagem_acesso == 'erro':
        mensagem_acesso = 'Ocorreu um erro no processo'
        msg_style = {'text-align': 'center', 'margin-top': '10px', 'color': 'red'}

    recuperar = dbc.Card(
        [
            html.Legend('Cadastro de nova senha'),
            dbc.Input(id='input_cod_validacao', placeholder='Insira o Código recebido', type='text',
                      style={'margin-top': '10px'}),
            dbc.Input(id='input_registro_senha', placeholder='Insira uma senha', type='password',
                      style={'margin-top': '10px'}),
            dbc.Input(id='input_registro_senha_repetida', placeholder='Repita a mesma senha', type='password',
                      style={'margin-top': '10px'}),
            html.Span(mensagem_acesso, style=msg_style),

            dbc.Button('Mudar senha', id='botao_mudar_senha', style={'margin-top': '10px'}),
            html.Div([
                html.Label('Ou', style={'margin-right': '5px'}),
                dcc.Link('faça Login', href='/login'),
            ], style={'padding': '20px', 'display': 'flex', 'justify-content': 'center'}),

            html.Div([
                html.Label('Feito por CEAC/CPMC', style={'margin-right': '5px', 'textAlign': 'center',
                                                         'color': 'orange', 'fontSize': 14}),
            ], style={'padding': '20px', 'display': 'flex', 'justify-content': 'center'})
        ], color="secondary", outline=True,
        style=card_style)
    return recuperar


@app2.callback(
    Output('validacao-state', "data"),
    Input('botao_mudar_senha', 'n_clicks'),
    Input('input_cod_validacao','value'),
    Input('input_registro_senha','value'),
    Input('input_registro_senha_repetida','value'),
    Input('recupera-state', "data")
)
def sucesso_acesso(n_clicks, cod_enviado, senha, senha_repetida, cod_sistema):
    if n_clicks is None:
        raise PreventUpdate
    print('Acessando o sistema')
    cpf_usuario = cod_sistema.split('.')[2]
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
        # ==================#
        print('#/#/#/')
        print(cpf_usuario)
        print('#/#/#/')

        user = Users.query.filter_by(user_cpf=cpf_usuario).first()
        print(user)
        print(user.user_password)
        print(user.user_cpf)
        print(user.user_email)
        print(user.user_name)
        print(user.user_aprovado)
        dt_agora = datetime.datetime.utcnow() + datetime.timedelta(hours=-3)
        agora = dt_agora.strftime('%d/%m/%Y - %H:%M:%S')

        if cod_enviado == '11022009':
            mudanca = User_table.update().where(User_table.c.user_cpf == user.user_cpf).values(user_aprovado='s')
            conn = engine.connect()
            try:
                conn.execute(mudanca)
                dados = [user.user_cpf, user.user_name, user.user_password, 'LIBERAÇÃO', agora, 's']
                print(f'Sucesso na aprovação')
            except Exception as erro:
                print(f'Erro na aprovação do cadastro - {erro}')


        if cod_enviado == cod_sistema.split('.')[1] and cod_enviado != '11022009':
            if senha == senha_repetida:
                d1 = generate_password_hash(senha, method='sha256')
                mudanca = User_table.update().where(User_table.c.user_cpf == user.user_cpf).values(user_password=d1)
                conn = engine.connect()
                try:
                    conn.execute(mudanca)
                    dados = [user.user_cpf, user.user_name, d1, 'MUDANÇA', agora]
                except Exception as erro:
                    print(f'Erro de atualização no SQL - {erro}')
            else:
                print('As senhas são fiderentes')
                return 'erro'
        else:
            print('O código de validação não foi aceito')
            print(cod_enviado)
            print(cod_sistema.split('.')[1])
            return 'erro'
        try:
            client = pygsheets.authorize(
                client_secret='client_secret_640793899938-gmj6mrgve57e9m79ir5i5tp258dsl9kt.'
                              'apps.googleusercontent.com.json')
            sh = client.open('Python_projetos')
            wks = sh.worksheet('title', '22 - Usuarios')
            wks.add_rows(1)
            linhas = len(wks.get_col(1))
            wks.update_row(linhas, dados)
        except Exception as erro:
            print(f'Erro ao tentar imprimir a mudança no WKS - {erro}')
        return f'Sucesso na mudança da senha/ liberação de acesso'

    except Exception as erro:
        print(f'Erro de - {erro}')
        return 'erro'
    conn.close()

