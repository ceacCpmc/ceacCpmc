from app2 import *
from datetime import date
from dash import Dash, html, dcc, dash_table
import plotly.express as px
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
import time
from dash_bootstrap_templates import load_figure_template, ThemeSwitchAIO
import numpy as np
from dash.exceptions import PreventUpdate
from flask_login import logout_user, current_user
import registra_log_saidas
from threading import Thread


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


def renderiza(usuario_atual):
    dados = dbc.Container(
        [
            html.Div([
                dcc.Location(id='data-url'),
                dbc.Row([
                    dbc.Col([
                        html.Br(),
                        dbc.Row([
                            dbc.Col([ThemeSwitchAIO(aio_id="theme", themes=[url_theme2, url_theme1],
                                       icons={"left": "fa fa-sun", "right": "fa fa-moon"})], md=6),
                            dbc.Col([
                                html.A(dbc.Button('Limpar filtros', id='botao_filtros',
                                           style={'textAlign': 'center'}, size='sm',
                                           outline=True, color="warning"), href='/dados'),

                            ], md=6),
                        ]),

                        html.Hr(),

                        html.H3('CEAC', style={'textAlign': 'center', 'margin': '15px'}),
                        # html.P('FONTE: SReports/CIOSP', className="text-success"),

                        html.H5('Registros', style={'textAlign': 'center',
                                                    # 'color': 'white'
                                                    'margin': '15px'}),

                        html.Div(id='total_acc'),

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
                        md=2),

                    dbc.Col([
                        html.H6('Bem-vindo, {}!'.format(usuario_atual), style={'textAlign': 'right',
                                                                               'fontSize': 16,
                                                                               'margin': '15px'}),
                        dbc.Row([
                            dbc.Col([
                                html.H1(children='ACIONAMENTOS 190', style={'textAlign': 'center'}),
                                html.P('Fonte: SReports / CIOSP',
                                       style={
                                           'textAlign': 'center',
                                           # 'color': 'green',
                                           'fontSize': 13,
                                           'margin-top': '-10px'}),
                            ],
                                md=11),
                            dbc.Col([
                                dbc.Button('Logoff', id='botao_logoff',
                                           style={'textAlign': 'right'}, size='sm',
                                           outline=True, color="warning"),
                            ], md=1),
                        ]),
                        html.Br(),
                        dbc.Row([
                            dbc.Col([dcc.Graph(id='gra_mes')], md=6),
                            dbc.Col([dcc.Graph(id='gra_opm')], md=6),
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
                            dbc.Col([dcc.Graph(id='gra_fim')], md=6),
                        ]),
                        html.Br(),
                        dbc.Row([
                            dbc.Col([dcc.Graph(id='gra_tipo')], md=6),
                            dbc.Col([dcc.Graph(id='gra_mun')], md=6)
                        ]),
                        html.Br(),
                        dbc.Row([
                            dbc.Col([dcc.Graph(id='gra_localidade')], md=12),
                            # dbc.Col([dcc.Graph(id='gra_radar')], md=3)
                        ]),
                        html.Br(),
                        dbc.Row([
                            dbc.Col([dcc.Graph(id='gra_mapa')], md=12),
                            # dbc.Col([dcc.Graph(id='gra_radar')], md=3)
                        ]),
                        # html.Br(),
                        # dbc.Row([
                        #     dbc.Col([dbc.Container([
                        #                 # dbc.Label('Click a cell in the table:'),
                        #                 dbc.Alert(id='tbl_out'),
                        #             ])
                        #         ], md=12),
                        #     # dbc.Col([dcc.Graph(id='gra_radar')], md=3)
                        # ]),
                        #
                    ],
                        md=10),
                ])  # LINHA MESTRE
            ])  # DIV MESTRE
        ],
        fluid=True,
        className="dbc"
    )
    return dados


# === CRIAÇÃO DAS FUNÇÕES E CALLBACK === #
@app2.callback(
    Output('data-url', 'pathname'),
    Input('botao_logoff', 'n_clicks')
)
def logoff(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    # if current_user.is_authenticated:
    print(current_user.user_name)
    a, b, c = current_user.user_name, current_user.user_cpf, current_user.user_email
    print(f' Estamos sainda da conta de - {a, b, c}')
    try:
        registra_log_saidas.registrar(a, b, c)
    except Exception as erro:
        print(f'Erro ao registrar logs de saída - {erro}')
    logout_user()
    return '/login'
    # else:
    #     return '/login'


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
        Output("loading-output-2", "children")

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
        Input('sel_cias', 'value')
    ])
def atualizar(mun, crime, historico, data_i, data_f, faixa_hora,
              dias_semana, selecao_finalizacao, opm, bairro_local, sub_tipo, toggle, inverso_intervalo, cias_sel):
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
    df_cidades = df_filtro['Municipio'].value_counts().to_frame().reset_index()
    df_cidades.columns = ['Municipio', 'Qtd']
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
                  category_orders={"Mes": ["JANEIRO", "FEVEREIRO", "MARCO", "ABRIL", "MAIO"]}, title="Série histórica",
                  template=template)

    fig2 = px.pie(df_opm, values='Qtd', names='OPM', hole=.3, title="OPM")

    fig3 = px.bar(df_turnos, x='Turno', y='Qtd', text='Qtd', title="Turnos",
                  category_orders={"Turno": ["00:00 AS 05:59", "06:00 AS 11:59", "12:00 AS 17:59", "18:00 AS 23:59"]})

    fig4 = px.bar(df_fim, x='Finalização', y='Qtd', orientation='v', text='Qtd', title="Finalizações")

    fig5 = px.bar(df_cidades, x="Municipio", y='Qtd', text='Qtd', title="Municípios")

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

    # fig8 = px.line_polar(df_tempo_medio, r='Qtd minutos aberta', theta='Hora da ligação', line_close=True)

    # fig_teste = px.scatter_mapbox(df_filtro, lat="Latitude", lon="Longitude", center=dict(lat=-10.9, lon=-37.06),
    #                               zoom=10, mapbox_style="open-street-map", height=900)
    # fig_teste.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    #####################################################

    # === ATUALIZAÇÃO DAS FIGURAS === #

    fig1.update_layout(margin=dict(l=10, r=10, t=40, b=10), height=250,
                       yaxis_title=None, xaxis_title=None)
    fig2.update_layout(margin=dict(l=10, r=10, t=40, b=10), height=250,
                       yaxis_title=None, xaxis_title=None)
    fig3.update_layout(margin=dict(l=10, r=10, t=40, b=10), height=250,
                       yaxis_title=None, xaxis_title=None)
    fig4.update_layout(margin=dict(l=10, r=10, t=40, b=10), height=250, uniformtext_minsize=8,  uniformtext_mode='hide',
                        yaxis_title=None, xaxis_title=None)

    fig5.update_layout(margin=dict(l=10, r=10, t=40, b=10), height=300,
                       uniformtext_minsize=6, uniformtext_mode='hide', yaxis_title=None, xaxis_title=None)
    fig6.update_traces(textposition='inside')
    fig6.update_layout(margin=dict(l=10, r=10, t=40, b=10), height=300,
                       uniformtext_minsize=8, uniformtext_mode='hide', yaxis_title=None, xaxis_title=None)
    fig7.update_layout(margin=dict(l=10, r=10, t=40, b=10), height=900)
    fig8.update_layout(margin=dict(l=10, r=10, t=40, b=10), height=300, yaxis_title=None, xaxis_title=None)

    # fig8.update_traces(fill='toself')
    # fig8.update_layout(margin=dict(l=10, r=10, t=40, b=10),height = 900, template = 'plotly_dark')

    print(f'Tempo para Atualizar o BD (após cada manipulação) - {time.time() - ti_alteracao}')

    del mask, df_filtro, df_mes, df_datas, df_fim, df_opm, \
        df_cidades, df_turnos, df_localidade, df_tipo, op, lista_historico

    return fig1, fig2, fig3, fig4, fig5, total_acionamentos, fig6, fig7, fig8, tempo  # , tabela
