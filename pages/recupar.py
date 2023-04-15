import random
import enviar_gmail
from app2 import *
from dash import Dash, html, dcc, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
from werkzeug.security import generate_password_hash


card_style = {
    'width': '300px',
    'min-height': '300px',
    'padding': '30px',
    'align-self': 'center'}


def renderiza(mensagem_acesso):
    msg_style = {'text-align': 'center', 'margin-top': '10px', 'color': 'red'}

    if mensagem_acesso == 'erro':
        mensagem_acesso = 'Usuário não cadastrado'

    if mensagem_acesso.__contains__('Sucesso'):
        mensagem_acesso = 'Um código de validação foi enviado para o email do usuário'


    recuperar = dbc.Card(
        [
            html.Legend('Recuperação de senha'),

            dbc.Input(id='input_cpf_recuperar', placeholder='Insira o CPF do usuário', type='text',
                      style={'margin-top': '10px'}),
            dbc.Button('Enviar', id='botao_recuperar', style={'margin-top': '10px'}),
            html.Br(),
            html.P('Após clicar em "ENVIAR" uma mensagem será encaminhada ao email cadastrado'
                   ' contendo um código de validação.'),
            html.Span(mensagem_acesso, style=msg_style),
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
    Output('recupera-state', "data"),
    Input('botao_recuperar', 'n_clicks'),
    Input('input_cpf_recuperar', 'value')
)
def sucesso_acesso(n_clicks, cpf_usuario):   # TODO: COLOCAR UMA LETRA PARA N ENVIAR O EMAIL EM CASO DA SENHA DE GESTOR
    if n_clicks is None:
        raise PreventUpdate
    try:
        # === RETIRAR === #
        # conn = sqlite3.connect('data.sqlite')
        # engine = create_engine('sqlite:///data.sqlite')

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

        a, b, c = user.user_name, user.user_cpf, user.user_email
        d = random.randint(1000, 9999)
        d1 = generate_password_hash(str(d), method='sha256')

        conn = engine.connect()
        try:
            pass
        except Exception as erro:
            print(f'Erro de atualização no SQL - {erro}')
        conn.close()

        print(f'Uma mensagem foi enviada para {a} para o email {c} alterando a senha do usuário de CFP {b}')
        print(f'A senha randônica criada foi {d}')
        try:
            enviar_gmail.enviar(a, d, c)
        except Exception as erro:
            print(f'Não foi possível enviar o email. Erro - {erro}')

        return f'Sucesso na recuperação.{d}.{b}'

    except Exception as erro:
        print(f'Erro de - {erro}')
        return 'erro'
