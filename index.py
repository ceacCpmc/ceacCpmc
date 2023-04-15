from app2 import *
import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
from pages import login, register, recupar, recuperar2, side_bar
from flask_login import current_user

login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'

# === CRIAÇÃO DO LAYOUT DA APLICAÇÃO === #


app2.layout = dbc.Container(
    [
        dbc.Row([
            dbc.Col([
                dcc.Location(id='endereco_url', refresh=False),

                # STORES de estados
                dcc.Store(id='registro-state', data=''),
                dcc.Store(id='login-state', data=''),
                dcc.Store(id='recupera-state', data=''),
                dcc.Store(id='validacao-state', data=''),
                dcc.Store(id='data-state', data=''),
                dcc.Store(id='tab-state', data=''),
                # Espaço principal onde tudo vai ser disposto
                html.Div(
                    id='conteudo_pag',
                    style={'height': '100vh',
                           'display': 'flex',
                           'justify-content': 'center'}
                ),
            ]),
        ])  # LINHA MESTRE
    ],
    fluid=True,
    className="dbc"
)


# === Callbacks === #


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app2.callback(
    Output("endereco_url", "pathname"),
    Input('login-state', "data"),
    Input('registro-state', "data"),
    Input('recupera-state', 'data'),
    Input('validacao-state','data')
)
def dinamica_url(login_state, registro_state, recupera_state, validacao_state):
    print(dash.callback_context.triggered)
    contexto_gatilho = dash.callback_context
    if contexto_gatilho.triggered:
        gatilho_id = contexto_gatilho.triggered[0]['prop_id'].split('.')[0]

        if gatilho_id == 'registro-state':
            if registro_state == 'OK':
                return '/registro'
            else:
                return '/registro'

        if gatilho_id == 'login-state':
            if login_state == 'Sucesso':
                return '/dados'
            if login_state == 'erro':
                return '/login'

        if gatilho_id == 'recupera-state':
            if recupera_state.__contains__('Sucesso'):
                return '/recuperar2'
            if recupera_state.__contains__('erro'):
                return '/recupar'


        # TODO: MUDAR PARA INSERIR SE A SENHA MUDADA COM SUCESSO ENVIAR PARA PÁGINA DE LOGIN


@app2.callback(
    Output("conteudo_pag", "children"),
    Input("endereco_url", "pathname"),
    [
        State('registro-state', "data"),
        State('login-state', "data"),
        State('recupera-state', 'data'),
        State('validacao-state', 'data'),
        State('data-state', 'data'),
        State('tab-state', 'data'),
    ]
)
def muda_url(pathname, registro_state, login_state, recupera_state, validacao_state, data_state, tab_state):
    print(registro_state)
    print(login_state)
    print(recupera_state)
    print(validacao_state)

    if pathname == '/login' or pathname == '/':
        if registro_state == 'OK':
            return login.renderiza(registro_state)
        if login_state == 'erro':
            return login.renderiza(login_state)
        else:
            return login.renderiza(login_state)

    if pathname == '/registro':
        return register.renderiza(registro_state)

    if pathname == '/recupar':
        return recupar.renderiza(recupera_state)

    if pathname == '/dados':
        if current_user.is_authenticated:
            # return data.renderiza(current_user.user_name)
            if tab_state == '':
                tab_state = '0'
            return side_bar.renderiza(current_user.user_name, data_state, tab_state)
        else:
            if registro_state == 'OK':
                return login.renderiza(registro_state)
            if login_state == 'erro':
                return login.renderiza(login_state)
            else:
                return login.renderiza(login_state)

    if pathname == '/recuperar2':
        return recuperar2.renderiza(validacao_state)


# === INICIALIZANDO A FUNÇÃO  main() === #

if __name__ == '__main__':
    app2.run_server(debug=True)
    # app.run_server(debug=True) # local
    # app.run_server(port=8051,debug=True)
