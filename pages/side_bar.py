import dash
from app2 import *
from datetime import date
from dash import Dash, html, dcc, dash_table
import plotly.express as px
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
import time
from dash_bootstrap_templates import load_figure_template, ThemeSwitchAIO
import numpy as np
from dash.exceptions import PreventUpdate
from flask_login import logout_user, current_user
import registra_log_saidas

template_theme1 = "flatly"
template_theme2 = "darkly"  # "darkly"
url_theme1 = dbc.themes.FLATLY
url_theme2 = dbc.themes.DARKLY

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

card_style = {
    # 'width': '300px',
    # 'min-height': '300px',
    'padding': '10px',
    'align-self': 'center'}

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 50.5,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "height": "92%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0.5rem 1rem",
    # "background-color": "#f8f9fa",
}

SIDEBAR_HIDEN = {
    "position": "fixed",
    "top": 50.5,
    "left": "-16rem",
    "bottom": 0,
    "width": "16rem",
    "height": "92%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0rem 0rem",
    # "background-color": "#f8f9fa",
}

CONTENT_STYLE = {

    "margin-left": "16rem",
    "margin-right": "2rem",
    "padding": "1rem 1rem",
    "position": "fixed",
    "top": 50.5,
    "left": 0,
    "bottom": 0,
    "width": "83%",
    "height": "95%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",

}

CONTENT_STYLE1 = {
    # "transition": "margin-left .5s",
    # "margin-left": "2rem",
    # "margin-right": "2rem",
    # "padding": "2rem 1rem",
    # "background-color": "#f8f9fa",
    "margin-left": "0rem",
    "margin-right": "2rem",
    "padding": "1rem 1rem",
    "position": "fixed",
    "width": "101%",
    "top": 50.5,
    "left": 0,
    "bottom": 0,
    "height": "95%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
}

tabs_styles = {
    'height': '35px'
}

tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '3px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '2px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    # 'backgroundColor': 'primary',
    # 'color': 'primary',       # TODO: AVALIAR AS CORES DE FUNDO E DE FONTE
    'padding': '3px'
}


def renderiza(usuario_atual, data_atualizada, tab):
    navbar = dbc.Navbar(
            [
                dbc.Container(
                    [
                        # html.A(
                            # Use row and col to control vertical alignment of logo / brand
                            dbc.Row(
                                [
                                    # dbc.Col(html.Img(src=app2.get_asset_url('ceac.png'), height="30px")),
                                    dbc.Col([dbc.NavbarBrand("CEAC", className="ms-2")],
                                            style={'textAlign': 'center'}, md=1),

                                    dbc.Col([
                                        dbc.Button("Filtros", id="btn_sidebar", style={'textAlign': 'letf'}, size='sm',
                                                   outline=False, color="primary"),  # className="mr-1",
                                    ], style={'textAlign': 'center'}, md=1),

                                    dbc.Col(
                                        [html.Div('ACIONAMENTOS 190'),
                                         ], style={'textAlign': 'center', 'fontSize': 26}, md=8),

                                    # dbc.Col([dbc.DropdownMenu(
                                    #     children=[
                                    #         # dbc.DropdownMenuItem("Opções", header=True),
                                    #         dbc.DropdownMenuItem("Mudar senha", href="/recupar"),
                                    #         dbc.DropdownMenuItem("Solicitar acesso", href="/registro"),
                                    #     ],
                                    #     nav=True,
                                    #     in_navbar=True,
                                    #     label="Opções")
                                    # ], style={'textAlign': 'left'}, md=1),

                                    dbc.Col([ThemeSwitchAIO(aio_id="theme", themes=[url_theme2, url_theme1],
                                        icons={"left": "fa fa-sun", "right": "fa fa-moon"})], md=1),

                                    dbc.Col([
                                        dbc.Button('Logoff', id='botao_logoff', style={'textAlign': 'right'}, size='sm',
                                       outline=False, color="warning")
                                    ],
                                        style={'textAlign': 'right'}, md=1),


                                ],
                                style={"width": "100%"},
                                    align="center",
                                    className="g-0",
                            ),
                        # href = "#",
                        # style = {"textDecoration": "none"}
                        # )
                    ], fluid=True)
            ],
            color="dark",
            dark=True,
            style={"height": "3rem","width": "100%", "position": "fixed","top": 0, "left": 0, "bottom": 0}
    )

    # the style arguments for the sidebar. We use position:fixed and a fixed width
    sidebar = dbc.Container(
                            [
                            # html.H2("Sidebar", className="display-4"),
                            # html.Hr(),
                            # html.P(
                            #     "A simple sidebar layout with navigation links", className="lead"
                            # ),
                            # dbc.Nav(
                            #     [
                            #         dbc.NavLink("Page 1", href="/page-1", id="page-1-link"),
                            #         dbc.NavLink("Page 2", href="/page-2", id="page-2-link"),
                            #         dbc.NavLink("Page 3", href="/page-3", id="page-3-link"),
                            #     ],
                            #     vertical=True,
                            #     pills=True,
                            # ),
                            # html.Br(),
                            dbc.Row([
                                html.Div([
                                    dcc.Tabs(id='tabs-example-1', value='tab-1',
                                    children=[
                                        dcc.Tab(label='Graf', value='tab-1', style=tab_style, selected_style=tab_selected_style),
                                        dcc.Tab(label='Mapa', value='tab-2', style=tab_style, selected_style=tab_selected_style),
                                        dcc.Tab(label='Tabela', value='tab-3', style=tab_style, selected_style=tab_selected_style),
                                    ], style=tabs_styles)
                                ])
                            ]),
                            html.Hr(),

                            dbc.Row([
                                dbc.Col([
                                    html.A(dbc.Button('Resetar todos filtros', id='botao_filtros',
                                                      style={'textAlign': 'center'}, size='sm',
                                                      outline=True, color="warning"), href='/dados'),

                                ], style={'textAlign': 'center'}, md=12),
                            ]),

                            html.Hr(),
                            # html.H3('CEAC', style={'textAlign': 'center', 'margin': '15px'}),
                            # html.P('FONTE: SReports/CIOSP', className="text-success"),

                            html.H5('Registros', style={'textAlign': 'center',
                                                        # 'color': 'white'
                                                        'margin': '15px'}),

                            html.Div(id='total_acc'),

                            html.Div(id='data_att'),

                            html.Hr(),

                            html.H6('OPM da área', style={'textAlign': 'left', 'margin': '15px'}),

                            dcc.Checklist(options={
                                '1BPM': '1BPM',
                                '5BPM': '5BPM',
                                '8BPM': '8BPM',
                                'BPTUR': 'BPTUR',
                                '1CIPM': '1CIPM',
                                '2CIPM': '2CIPM',
                                '3CIPM': '3CIPM',
                                '6CIPM': '6CIPM',
                            }, value=['1BPM', '5BPM', '8BPM', 'BPTUR',
                                      '1CIPM', '2CIPM', '3CIPM', '6CIPM'],
                                id='sel_opm', inputStyle={"margin-right": "10px", "margin-left": "10px"}),

                            html.Hr(),

                            html.H6('Cia da área', style={'textAlign': 'left', 'margin': '15px'}),
                            dcc.Dropdown(cias, ['TODAS'], id='sel_cias', placeholder="Selecione as Companhias..",
                                         style={'dropdown-content': '{padding: 8px}'}, multi=True),

                            html.Hr(),

                            html.H6('Municípios', style={'textAlign': 'left', 'margin': '15px'}),
                            dcc.Dropdown(municip, ['TODOS'], id='sel_mun', placeholder="Selecione municípios...",
                                         style={'dropdown-content': '{padding: 8px}'}, multi=True),
                            html.Hr(),

                            html.H6('Localidades', style={'textAlign': 'left', 'margin': '15px'}),
                            dcc.Dropdown(bairros, ['TODOS'], id='sel_bairros',
                                         placeholder="Selecione a localidade...",
                                         style={'dropdown-content': '{padding: 8px}'}, multi=True),
                            html.Hr(),

                            html.H6('Tipo de crime', style={'textAlign': 'left', 'margin': '15px'}),

                            dcc.Dropdown(tipos_descricao,
                                         ['ROUBO', 'FURTO', 'HOMICIDIO'], id='sel_descricao',
                                         placeholder="Selecione tipos...",
                                         style={'dropdown-content': '{padding: 8px; font-size: 8px}'}, multi=True),
                            html.Hr(),

                            html.H6('Sub Tipo de crime',
                                    style={'textAlign': 'left', 'margin': '15px'}),

                            dcc.Dropdown(sub_tipos_descricao,
                                         ['TODOS'], id='sel_sub_tipo',
                                         placeholder="Selecione o sub tipos...",
                                         style={'dropdown-content': '{padding: 8px; font-size: 8px}'},
                                         multi=True),
                            html.Hr(),

                            html.H6('Tipo de finalização',
                                    style={'textAlign': 'left', 'margin': '15px'}),

                            dcc.Dropdown(tipos_finalizacao,
                                         ['TODOS'],
                                         id='sel_fim',
                                         placeholder="Selecione tipos...",
                                         style={'dropdown-content': '{padding: 8px; font-size: 8px}'},
                                         multi=True),
                            html.Hr(),

                            html.H6('Faixa de horário',
                                    style={'textAlign': 'left', 'margin': '15px'}),

                            dcc.RangeSlider(0, 23, 1, marks=None, value=[0, 23], id='faixa_horario',
                                            tooltip={"placement": "bottom", "always_visible": True}),

                            dcc.Checklist(['Inverso do intervalo'], [], id='inverso',
                                          style={"color": "red"}, inputStyle={"margin-right": "10px",
                                                                              "margin-left": "10px"}),
                            html.Hr(),

                            html.H6('Dias da Semana',
                                    style={'textAlign': 'left', 'margin': '15px'}),

                            dcc.Checklist(
                                options={
                                    'SEGUNDA': 'SEG',
                                    'TERCA': 'TER',
                                    'QUARTA': 'QUA',
                                    'QUINTA': 'QUI',
                                    'SEXTA': 'SEX',
                                    'SABADO': 'SAB',
                                    'DOMINGO': 'DOM'},
                                value=['SEGUNDA', 'TERCA', 'QUARTA', 'QUINTA',
                                       'SEXTA', 'SABADO', 'DOMINGO'], id='dias_semana',
                                inputStyle={"margin-right": "10px",
                                            "margin-left": "10px"}
                            ),
                            html.Hr(),

                            html.H6('Período de busca',
                                    style={'textAlign': 'left', 'margin': '15px'}),

                            dcc.DatePickerRange(
                                id='janela_tempo',
                                start_date=date(2022, 1, 1),
                                end_date=date(2022, 12, 31),
                                start_date_placeholder_text="Data_Inicial",
                                end_date_placeholder_text="Data_Final",
                                calendar_orientation='vertical',
                                display_format='DD MM YY'
                            ),
                            html.Hr(),

                            html.H6('Busca no histórico',
                                    style={'textAlign': 'left', 'margin': '15px'}),

                            dcc.Input(
                                placeholder='Digite aqui...',
                                type='text',
                                value='',
                                id='sel_historico'),
                            html.Hr(),
                            ],
                        fluid=True,
                        className="dbc",
                        id="sidebar",
                        style=SIDEBAR_STYLE
                    )



    layout = html.Div(
                            [
                                dcc.Store(id='side_click'),
                                dcc.Store(id='tab-state', data=''),
                                dcc.Location(id='data-url'),
                                navbar,
                                sidebar,
                                html.Div(id='conteudo_tabs'), #content
                            ]
                        )
    return layout


# CALL BACKS #

@app2.callback(Output('conteudo_tabs', 'children'),
              Input('tabs-example-1', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        content = dbc.Container(
            [
                dbc.Row([
                    dbc.Col([html.H6('Bem-vindo, {}!'.format(current_user.user_name), style={'textAlign': 'right',
                                                                                             'fontSize': 16,
                                                                                             'margin': '15px'})],
                            md=12),

                ]),
                dbc.Row([
                    dbc.Col([dcc.Graph(id='gra_mes')], md=6),
                    dbc.Col([dcc.Graph(id='gra_opm')], md=6)
                ]),
                html.Br(),
                dbc.Row([
                    dbc.Col(
                        [
                            html.Div(
                                dcc.Loading(
                                    id="loading-2",
                                    type="dot",
                                    children=html.Div(id="loading-output-2"),
                                    # className='spinner',
                                    style={'margin-top': '-13px'}
                                )
                            )
                        ],
                        md=12),
                ]),

                dbc.Row([
                    dbc.Col([dcc.Graph(id='gra_turno')], md=6),
                    dbc.Col([dcc.Graph(id='gra_cia')], md=6)
                ]),
                html.Br(),

                dbc.Row([
                    dbc.Col([dcc.Graph(id='gra_tipo')], md=6),
                    dbc.Col([dcc.Graph(id='gra_fim')], md=6)
                ]),
                html.Br(),

                dbc.Row([
                    dbc.Col([dcc.Graph(id='gra_mun')], md=6),
                    dbc.Col([dcc.Graph(id='gra_localidade')], md=6)
                    # dbc.Col([dcc.Graph(id='gra_radar')], md=3)
                ]),

                html.Br(),

                html.Div([
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id='gra_mapa')
                        ], md=12)
                    ])
                ], style={'display':'none'}),

                dbc.Row([
                    dbc.Col([
                        html.Div(id='id_tabela',style={'display':'none'})
                     ], md=12),
                ]),


            ],
            fluid=True,
            className="dbc",
            id="page-content",
            style=CONTENT_STYLE
        )
        return content

    # if tab == 'tab-2':
    #     content_mapa = dbc.Container([
    #     dbc.Row([
    #         dbc.Col([dcc.Graph(id='gra_mapa')], md=12),
    #     ]),
    # ],
    #     fluid=True,
    #     className="dbc",
    #     id="page-content_mapa",
    #     style=CONTENT_STYLE
    #     )
    #     return content_mapa
    #
    # if tab == 'tab-3':
    #     content_tabela = dbc.Container([
    #         dbc.Row([
    #             dbc.Col([
    #                 html.Div(id='id_tabela'),
    #     ], md=12),
    #         ]),
    #     ],
    #         fluid=True,
    #         className="dbc",
    #         id="page-content_tabela",
    #         style=CONTENT_STYLE
    #     )
    #     return content_tabela

    if tab == 'tab-2':
        content_mapa = dbc.Container(
            [
                html.Div([
                    dbc.Row([
                        dbc.Col([dcc.Graph(id='gra_mes')], md=6),
                        dbc.Col([dcc.Graph(id='gra_opm')], md=6)
                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col(
                            [
                                html.Div(
                                    dcc.Loading(
                                        id="loading-2",
                                        type="dot",
                                        children=html.Div(id="loading-output-2"),
                                        # className='spinner',
                                        style={'margin-top': '-13px'}
                                    )
                                )
                            ],
                            md=12),
                    ]),
                    dbc.Row([
                        dbc.Col([dcc.Graph(id='gra_turno')], md=6),
                        dbc.Col([dcc.Graph(id='gra_cia')], md=6)
                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col([dcc.Graph(id='gra_tipo')], md=6),
                        dbc.Col([dcc.Graph(id='gra_fim')], md=6)
                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col([dcc.Graph(id='gra_mun')], md=6),
                        dbc.Col([dcc.Graph(id='gra_localidade')], md=6)
                        # dbc.Col([dcc.Graph(id='gra_radar')], md=3)
                    ]),
                    html.Br(),
                ],style={'display':'none'}),

                dbc.Row([
                    dbc.Col([
                        html.Div([dcc.Graph(id='gra_mapa')], style={'display':'block'})
                    ], md=12)
                ]),

                dbc.Row([
                    dbc.Col([
                        html.Div(id='id_tabela',style={'display':'none'})
                     ], md=12),
                ]),


            ],
            fluid=True,
            className="dbc",
            id="page-content",
            style=CONTENT_STYLE
        )
        return content_mapa

    if tab == 'tab-3':
        content_tabela = dbc.Container(
            [
                html.Div([
                    dbc.Row([
                        dbc.Col([dcc.Graph(id='gra_mes')], md=6),
                        dbc.Col([dcc.Graph(id='gra_opm')], md=6)
                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col(
                            [
                                html.Div(
                                    dcc.Loading(
                                        id="loading-2",
                                        type="dot",
                                        children=html.Div(id="loading-output-2"),
                                        # className='spinner',
                                        style={'margin-top': '-13px'}
                                    )
                                )
                            ],
                            md=12),
                    ]),
                    dbc.Row([
                        dbc.Col([dcc.Graph(id='gra_turno')], md=6),
                        dbc.Col([dcc.Graph(id='gra_cia')], md=6)
                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col([dcc.Graph(id='gra_tipo')], md=6),
                        dbc.Col([dcc.Graph(id='gra_fim')], md=6)
                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col([dcc.Graph(id='gra_mun')], md=6),
                        dbc.Col([dcc.Graph(id='gra_localidade')], md=6)
                        # dbc.Col([dcc.Graph(id='gra_radar')], md=3)
                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col([
                            html.Div([dcc.Graph(id='gra_mapa')], style={'display': 'block'})
                        ], md=12)
                    ]),
                ], style={'display': 'none'}),

                dbc.Row([
                    dbc.Col([
                        html.Div(id='id_tabela', style={'display': 'block'})
                    ], md=12),
                ]),
            ],
            fluid=True,
            className="dbc",
            id="page-content",
            style=CONTENT_STYLE
        )
        return content_tabela


@app2.callback(
    [
        Output("sidebar", "style"),
        Output("page-content", "style"),
        Output("side_click", "data"),
    ],

    [Input("btn_sidebar", "n_clicks")],
    [
        State("side_click", "data"),
    ]
)
def toggle_sidebar(n, nclick):
    print(dash.callback_context.triggered)
    contexto_gatilho = dash.callback_context
    sidebar_style = SIDEBAR_STYLE
    content_style = CONTENT_STYLE
    if contexto_gatilho.triggered:
        gatilho_id = contexto_gatilho.triggered[0]['prop_id'].split('.')[0]

        if gatilho_id == 'btn_sidebar':
            if n:
                if nclick == "SHOW":
                    sidebar_style = SIDEBAR_HIDEN
                    content_style = CONTENT_STYLE1
                    cur_nclick = "HIDDEN"
                else:
                    sidebar_style = SIDEBAR_STYLE
                    content_style = CONTENT_STYLE
                    cur_nclick = "SHOW"
            else:
                sidebar_style = SIDEBAR_STYLE
                content_style = CONTENT_STYLE
                cur_nclick = "SHOW"

    return sidebar_style, content_style, cur_nclick


@app2.callback(
    Output('data-url', 'pathname'),
    Input('botao_logoff', 'n_clicks'),
)
def logoff(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    print(current_user.user_name)
    a, b, c = current_user.user_name, current_user.user_cpf, current_user.user_email
    print(f' Estamos sainda da conta de - {a, b, c}')
    try:
        registra_log_saidas.registrar(a, b, c)
        logout_user()
    except Exception as erro:
        print(f'Erro ao registrar logs de saída - {erro}')
        return '/erro'
    return '/login'


@app2.callback(
    [
        Output('gra_mes', 'figure'),
        Output('gra_opm', 'figure'),
        Output('gra_turno', 'figure'),
        Output('gra_fim', 'figure'),
        Output('gra_mun', 'figure'),
        Output('total_acc', 'children'),
        Output('gra_tipo', 'figure'),
        Output('gra_mapa', 'figure'),
        Output('gra_localidade', 'figure'),
        Output("loading-output-2", "children"),
        Output("gra_cia", "figure"),
        Output('data_att','children'),
        Output('tab-state', 'data'),
        Output('id_tabela', 'children')

        # Output('tbl_out', 'children')
        # Output('gra_radar', 'figure')
    ],

    [
        Input('sel_mun', 'value'),
        Input('sel_descricao', 'value'),
        Input('sel_historico', 'value'),
        Input('janela_tempo', 'start_date'),
        Input('janela_tempo', 'end_date'),
        Input('faixa_horario', 'value'),
        Input('dias_semana', 'value'),
        Input('sel_fim', 'value'),
        Input('sel_opm', 'value'),
        Input('sel_bairros', 'value'),
        Input('sel_sub_tipo', 'value'),
        Input(ThemeSwitchAIO.ids.switch("theme"), "value"),
        Input('inverso', 'value'),
        Input('sel_cias', 'value'),
        Input("side_click", "data"),
        Input('tabs-example-1', 'value'),
    ])
def atualizar(mun, crime, historico, data_i, data_f, faixa_hora,
              dias_semana, selecao_finalizacao, opm, bairro_local,
              sub_tipo, toggle, inverso_intervalo, cias_sel, side_visivel, tab):

    if tab == 'tab-1' or tab == '':
        aba = '0'

    elif tab == 'tab-2':
        aba = '1'

    elif tab =='tab-3':
        aba = '2'
    print(f'O valor da aba é {aba}, porque o valor da tab foi {tab}')
    print(side_visivel)
    data_atualizada = df['Data_de_Criacao'].iloc[-1]
    template = template_theme2 if toggle else template_theme1
    load_figure_template(template)
    ti_alteracao = time.time()
    mask = (df['Novo_tempo2'] >= data_i) & (df['Novo_tempo2'] <= data_f)
    df_filtro = df.loc[mask]
    if len(inverso_intervalo) > 0:
        print('Inverso ativado')
        mask = (df_filtro['Hora_int'] < faixa_hora[0]) | (df_filtro['Hora_int'] > faixa_hora[1])
    else:
        mask = (df_filtro['Hora_int'] >= faixa_hora[0]) & (df_filtro['Hora_int'] <= faixa_hora[1])
    df_filtro = df_filtro.loc[mask]
    # print(crime)
    # print(historico)
    historico = historico.replace(' ', '')
    lista_historico = historico.split(',')
    del historico
    tempo = ''
    try:
        lista_historico.remove('')
    except Exception as erro:
        print(f'Erro de - {erro}')
        pass
    print(lista_historico)
    if 'TODOS' in mun:
        mun = municip

    if 'TODOS' in crime:
        crime = tipos_descricao

    if 'TODOS' in selecao_finalizacao:
        selecao_finalizacao = tipos_finalizacao

    if 'TODOS' in bairro_local:
        bairro_local = bairros

    if 'TODOS' in sub_tipo:
        sub_tipo = sub_tipos_descricao

    if 'TODAS' in cias_sel:
        cias_sel = cias

    op = np.count_nonzero
    df_filtro = df_filtro[df_filtro["Municipio"].isin(mun)]
    df_filtro = df_filtro[df_filtro['BPM_NOVO'].isin(opm)]
    df_filtro = df_filtro[df_filtro['BAIRRO_NOVO'].isin(bairro_local)]
    df_filtro = df_filtro[df_filtro["Desc._Sub_Tipo"].isin(sub_tipo)]
    df_filtro = df_filtro[df_filtro["Descricao_Finalizacao"].isin(selecao_finalizacao)]
    df_filtro = df_filtro[df_filtro["DIA_DA_SEMANA"].isin(dias_semana)]
    df_filtro = df_filtro[df_filtro["DESCRICAO_OK"].isin(crime)]
    df_filtro = df_filtro.drop(df_filtro[df_filtro['Historico'].isna()].index)
    df_filtro = df_filtro[df_filtro['Historico'].str.contains('|'.join(lista_historico), case=False)]
    df_filtro = df_filtro[df_filtro["Cia"].isin(cias_sel)]

    # ----------------------------------------------------------------------------------- df_tempo_medio =
    # df_filtro.groupby(['Intervalo_aberta_fechada', 'Hora_int_textual'])[['XCORD']].apply(op).reset_index()
    # df_tempo_medio.columns = ['Qtd minutos aberta', 'Hora da ligação','Qtd']

    df_cidades = df_filtro.groupby(['Municipio', 'DESCRICAO_OK'], group_keys=True)[['XCORD']].apply(op).reset_index()

    # df_cidades = df_filtro['Municipio'].value_counts().to_frame().reset_index()
    df_cidades.columns = ['Municipio', 'Tipo','Qtd']


    df_tipo = df_filtro['DESCRICAO_OK'].value_counts().to_frame().reset_index()
    df_tipo.columns = ['Tipo', 'Qtd']
    df_datas = df_filtro['Data_de_Criacao'].value_counts().to_frame().reset_index()
    df_datas.columns = ['Data', 'Qtd']
    df_fim = df_filtro['Descricao_Finalizacao'].value_counts().to_frame().reset_index()
    df_fim.columns = ['Finalização', 'Qtd']
    df_mes = df_filtro.groupby(['Municipio', 'MES'])[['XCORD']].apply(op).reset_index()
    df_mes.columns = ['Municipio', 'Mes', 'Qtd']
    df_turnos = df_filtro['FAIXA_6HS'].value_counts().to_frame().reset_index()
    df_turnos.columns = ['Turno', 'Qtd']
    df_opm = df_filtro.groupby(['Municipio', 'BPM_NOVO'])[['XCORD']].apply(op).reset_index()
    df_opm.columns = ['Municipio', 'OPM', 'Qtd']
    df_localidade = df_filtro['BAIRRO_NOVO'].value_counts().to_frame().reset_index()
    df_localidade.columns = ['Localidade', 'Qtd']
    df_localidade = df_localidade.head(20)
    df_cia = df_filtro['Cia'].value_counts().to_frame().reset_index()
    df_cia.columns = ['Cia', 'Qtd']


    total_190 = len(df_filtro.index)
    total_geral = len(df.index)

    total_acionamentos = [html.P('{0:,.0f}'.format(total_190),
                                 style={'textAlign': 'center',
                                        'color': 'orange',
                                        'fontSize': 40}),

                          html.P(
                              str(round((total_190 / total_geral) * 100, 2)) + '% de '
                              + '{0:,.0f}'.format(total_geral)
                              + ' protocolos',
                              style={
                                  'textAlign': 'center',
                                  'color': 'green',
                                  'fontSize': 15,
                                  'margin-top': '-18px'})
                          ]

    # tabela = dash_table.DataTable(df_mes.to_dict('records'),[{"name": i, "id": i} for i in df_mes.columns], id='tbl'),

    fig1 = px.bar(df_mes, x='Mes', y='Qtd', color='Municipio', barmode='group',
                  category_orders={"Mes": ["JANEIRO", "FEVEREIRO", "MARCO", "ABRIL", "MAIO", "JUNHO",
                                           "JULHO", "AGOSTO", 'SETEMBRO', 'OUTUBRO', "NOVEMBRO", "DEZEMBRO"]},
                  title="Série histórica",
                  template=template)

    fig2 = px.pie(df_opm, values='Qtd', names='OPM', hole=.3, title="OPM")

    fig3 = px.bar(df_turnos, x='Turno', y='Qtd', text='Qtd', title="Turnos",
                  category_orders={"Turno": ["00:00 AS 05:59", "06:00 AS 11:59", "12:00 AS 17:59", "18:00 AS 23:59"]})

    fig4 = px.bar(df_fim, x='Finalização', y='Qtd', orientation='v', text='Qtd', title="Finalizações")

    fig5 = px.bar(df_cidades, x="Municipio", y='Qtd', color='Tipo', text='Qtd', title="Municípios", barmode='group') #

    fig6 = px.pie(df_tipo, values='Qtd', names='Tipo', hole=0.3, title="Tipo")

    fig7 = px.density_mapbox(df_filtro, lat='Latitude', lon='Longitude', z='Peso_crimes', radius=70,
                             center=dict(lat=-10.9, lon=-37.06), zoom=10, hover_name="DESCRICAO_OK",
                             hover_data={'Latitude': False, 'Longitude': False, 'Peso_crimes': False,
                                         'Ocorrencia': True,
                                         'Data': True, 'Hora': True,
                                         'Cia': True, 'Viatura': True
                                         },
                             mapbox_style="open-street-map",
                             color_continuous_scale=[
                                 [0.0, "white"],
                                 [0.30, "green"],
                                 [0.50, "yellow"],
                                 [0.70, "orange"],
                                 [0.90, "red"],
                                 [1.0, "red"]],
                             opacity=0.6
                             )

    # fig7 = px.scatter_mapbox(lat=df_filtro['Latitude']
    #                       , lon=df_filtro['Longitude']
    #                       , size=5
    #                       # , marker_color='rgb(0, 0, 0)'
    #                       # , #showlegend=False,
    #                        ,opacity=0.6)

    # fig7.add_densitymapbox(df_filtro, lat='Latitude', lon='Longitude', z='Peso_crimes' ,radius=70,
    #                         center=dict(lat=-10.9, lon=-37.06), zoom=10, hover_name="DESCRICAO_OK",
    #                         hover_data={'Latitude':False, 'Longitude':False, 'Peso_crimes':False,
    #                                     'Ocorrencia':True,
    #                                     'Data':True, 'Hora':True,
    #                                     'Cia':True, 'Viatura':True
    #                                      },
    #                         mapbox_style="open-street-map",
    #                          color_continuous_scale=[
    #                              [0.0, "white"],
    #                              [0.30, "green"],
    #                              [0.50, "yellow"],
    #                              [0.70, "orange"],
    #                              [0.90, "red"],
    #                              [1.0, "red"]],
    #                          opacity=0.45)

    # fig7.add_scattermapbox(lat=df_filtro['Latitude']
    #                       , lon=df_filtro['Longitude']
    #                       , hoverinfo= 'none'
    #                       , marker_size=5
    #                       , marker_color='rgb(0, 0, 0)'
    #                       , #showlegend=False,
    #                        opacity=0.6
    #                       )

    fig8 = px.bar(df_localidade, x="Localidade", y='Qtd', text='Qtd', title="Localidades (20 maiores frequências)")

    fig9 = px.bar(df_cia, x='Cia', y='Qtd', text='Qtd', title='Sub Unidade')

    # fig8 = px.line_polar(df_tempo_medio, r='Qtd minutos aberta', theta='Hora da ligação', line_close=True)

    # fig_teste = px.scatter_mapbox(df_filtro, lat="Latitude", lon="Longitude", center=dict(lat=-10.9, lon=-37.06),
    #                               zoom=10, mapbox_style="open-street-map", height=900)
    # fig_teste.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    #####################################################

    # === ATUALIZAÇÃO DAS FIGURAS === #

    fig1.update_layout(margin=dict(l=10, r=10, t=40, b=10), height=300,
                       yaxis_title=None, xaxis_title=None)
    fig2.update_layout(margin=dict(l=10, r=10, t=40, b=10), height=300,
                       yaxis_title=None, xaxis_title=None)
    fig3.update_layout(margin=dict(l=10, r=10, t=40, b=10), height=300,
                       yaxis_title=None, xaxis_title=None)
    fig4.update_layout(margin=dict(l=10, r=10, t=40, b=10), height=300, uniformtext_minsize=8,  uniformtext_mode='hide',
                        yaxis_title=None, xaxis_title=None)

    fig5.update_layout(margin=dict(l=10, r=10, t=40, b=10), height=300,
                       uniformtext_minsize=6, uniformtext_mode='hide', yaxis_title=None, xaxis_title=None)
    fig5.update_xaxes(categoryorder='total descending')
    fig5.update_layout(legend_traceorder='normal')

    fig6.update_traces(textposition='inside')
    fig6.update_layout(margin=dict(l=10, r=10, t=40, b=10), height=300,
                       uniformtext_minsize=8, uniformtext_mode='hide', yaxis_title=None, xaxis_title=None)
    fig7.update_layout(margin=dict(l=10, r=10, t=40, b=10), height=900)
    fig8.update_layout(margin=dict(l=10, r=10, t=40, b=10), height=300, yaxis_title=None, xaxis_title=None)
    fig9.update_layout(margin=dict(l=10, r=10, t=40, b=10), height=300,
                       yaxis_title=None, xaxis_title=None)


    # fig8.update_traces(fill='toself')
    # fig8.update_layout(margin=dict(l=10, r=10, t=40, b=10),height = 900, template = 'plotly_dark')

    print(f'Tempo para Atualizar o BD (após cada manipulação) - {time.time() - ti_alteracao}')

    data_atualizada = html.H6('Registros até {}'.format(data_atualizada), style={'textAlign': 'center',
                                                            'fontSize': 10,
                                                            'margin': '15px'})

    lista_colunas_tabela = ['MES', 'Data_de_Criacao', 'DIA_DA_SEMANA','Hora' , 'Ocorrencia', 'Municipio', 'DESCRICAO_OK',
                            'Desc._Sub_Tipo', 'BAIRRO_NOVO', 'Descricao_Finalizacao']

    df_tabela = df_filtro[lista_colunas_tabela]
    df_tabela.columns = ['Mes', 'Data', 'Dia', 'Hora', 'Protocolo', 'Municipio', 'Tipo', 'Sub Tipo', 'Bairro',
                         'Finalização']


    tabela = dash_table.DataTable(data=df_tabela.to_dict('records'),
                                  columns=[{"name": i, "id": i} for i in df_tabela.columns],
                                  sort_action='native',
                                  # filter_action='native',
                                  fixed_rows={'headers': True},
                                  style_data={
                                      'whiteSpace': 'normal',
                                      'height': 'auto'},
                                  style_table={'overflowX': 'auto', 'height': 'auto'}, #'height': 400, 'overflowY': 'auto'
                                  style_cell={'minWidth': 40, 'maxWidth': 95, 'width': 40, 'textAlign': 'center'},
                                  style_header={'fontWeight': 'bold', 'backgroundColor': 'secundary'},
                                  )

    del mask, df_filtro, df_mes, df_datas, df_fim, df_opm, \
        df_cidades, df_turnos, df_localidade, df_tipo, op, lista_historico, df_tabela

    return fig1, fig2, fig3, fig4, fig5, total_acionamentos, fig6, fig7, fig8, tempo, fig9, data_atualizada, aba, tabela # , tabela

