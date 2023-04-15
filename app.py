import os
from datetime import date
import dash_auth.auth
from dash import Dash, html, dcc, dash_table
import plotly.express as px
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
import numpy as np
import pandas as pd
import utm
import time
import dash_auth
from dash_bootstrap_templates import load_figure_template, ThemeSwitchAIO

template_theme1 = "litera"
template_theme2 = "cyborg" #"darkly"
url_theme1 = dbc.themes.LITERA
url_theme2 = dbc.themes.CYBORG

dbc_css = ("https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css")

VALID_USERNAME_PASSWORD_PAIRS = {
    'ceac': '1234',
    'planejamento':'4321',
    'em':'1972',
    '1bpm':'8194',
    '5bpm':'7238',
    '8bpm':'5490',
    'bptur': '1950',
    '1cipm': '3026',
    '2cipm': '6209',
    '3cipm': '7813',
    '6cipm': '2471',
}

t1 = time.time()

# TODO: Retirar esses @profile
def pesos_crime(row):
    if row['SITUACAO_SENASP'] =='CVLI':
        return 80
    elif row['SITUACAO_SENASP'] =='CVNLI':
        return 20
    elif row['SITUACAO_SENASP'] =='CVP':
        return 15
    elif row['SITUACAO_SENASP'] =='CNVP':
        return 5
    elif row['SITUACAO_SENASP'] =='CVNP':
        return 5
    return 1

def hora_int(row):
    if row['FAIXA_HORARIA'] =='00:00':
        return 0
    elif row['FAIXA_HORARIA'] =='01:00':
        return 1
    elif row['FAIXA_HORARIA'] =='02:00':
        return 2
    elif row['FAIXA_HORARIA'] =='03:00':
        return 3
    elif row['FAIXA_HORARIA'] =='04:00':
        return 4
    elif row['FAIXA_HORARIA'] =='05:00':
        return 5
    elif row['FAIXA_HORARIA'] =='06:00':
        return 6
    elif row['FAIXA_HORARIA'] =='07:00':
        return 7
    elif row['FAIXA_HORARIA'] =='08:00':
        return 8
    elif row['FAIXA_HORARIA'] =='09:00':
        return 9
    elif row['FAIXA_HORARIA'] =='10:00':
        return 10
    elif row['FAIXA_HORARIA'] =='11:00':
        return 11
    elif row['FAIXA_HORARIA'] =='12:00':
        return 12
    elif row['FAIXA_HORARIA'] =='13:00':
        return 13
    elif row['FAIXA_HORARIA'] =='14:00':
        return 14
    elif row['FAIXA_HORARIA'] =='15:00':
        return 15
    elif row['FAIXA_HORARIA'] =='16:00':
        return 16
    elif row['FAIXA_HORARIA'] =='17:00':
        return 17
    elif row['FAIXA_HORARIA'] =='18:00':
        return 18
    elif row['FAIXA_HORARIA'] =='19:00':
        return 19
    elif row['FAIXA_HORARIA'] =='20:00':
        return 20
    elif row['FAIXA_HORARIA'] =='21:00':
        return 21
    elif row['FAIXA_HORARIA'] =='22:00':
        return 22
    return 23

app = Dash(__name__, external_stylesheets=[url_theme1, dbc_css])
auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)
server = app.server

# === CRIAÇÃO DE VARIÁVEIS DO SISTEMA === #

df = pd.read_excel('base.xlsx')  # mudar entre base_teste.xlsx e base.xlsx
print(f'Tempo para ler o BD - {time.time() - t1}')

df.drop(df.loc[df['Fechado'] == '// ::'].index, inplace=True)
municip = ['TODOS', 'ARACAJU', 'NOSSA SENHORA DO SOCORRO', 'BARRA DOS COQUEIROS',
           'ITAPORANGA DAJUDA', 'SAO CRISTOVAO', 'MARUIM', 'LARANJEIRAS',
           'RIACHUELO', 'SANTO AMARO DAS BROTAS', 'DIVINA PASTORA']
# cias = ['1CIA/1BPM', '2CIA/1BPM', '3CIA/1BPM']
dias_semana = ['SEG', 'TER', 'QUA', 'QUI', 'SEX', 'SAB', 'DOM']
tipos_descricao = list(set(df['DESCRICAO_OK'].to_list()))
cleanedList = [x for x in tipos_descricao if str(x) != 'nan']
tipos_descricao = cleanedList
tipos_descricao.append('TODOS')
df['Desc._Sub_Tipo'] = df['Desc._Sub_Tipo'].fillna('Sem sub tipo')
df['Viatura'] = df['Viatura'].fillna(' - x - ')

sub_tipos_descricao = list(set(df['Desc._Sub_Tipo'].to_list()))
cleanedList = [x for x in sub_tipos_descricao if str(x) != 'nan']
sub_tipos_descricao = cleanedList
sub_tipos_descricao.append('TODOS')
del(cleanedList)

bairros = list(set(df['BAIRRO_NOVO'].to_list()))
bairros.append('TODOS')
cias_temp = []
df['Cia'] = df['CIA_NOVA']
cias = list(set(df['Cia'].to_list()))
cleanedList = [x for x in cias if str(x) != 'nan']
cias = cleanedList
del(cleanedList)
for i in cias:
    if i.count('/1BPM'):
        cias_temp.append(i)
    if i.count('/5BPM'):
        cias_temp.append(i)
    if i.count('/8BPM'):
        cias_temp.append(i)
    if i.count('/BPTUR'):
        cias_temp.append(i)
    if i.count('1CIPM'):
        cias_temp.append(i)
    if i.count('2CIPM'):
        cias_temp.append(i)
    if i.count('3CIPM'):
        cias_temp.append(i)
    if i.count('6CIPM'):
        cias_temp.append(i)
cias = cias_temp
cias.append('TODAS')

tipos_finalizacao = list(set(df['Descricao_Finalizacao'].to_list()))
tipos_finalizacao.append('TODOS')
try:
    tipos_finalizacao.pop(0)
except Exception as erro:
    print(f'Erro de - {erro}')
    pass


df['Peso_crimes'] = df.apply(lambda row: pesos_crime(row), axis=1)
df['Hora_int'] = df.apply(lambda row: hora_int(row), axis=1)
df['Hora'] = df['Aberto'].astype(str)
df['Hora'] = df.Hora.str[11:]
df['Data'] = df.Data_de_Criacao.str[:10]
df['Novo_tempo2'] = pd.to_datetime(df['Data'], format='%d/%m/%Y')
df.drop(df.loc[df['XCORD'] == 0].index, inplace=True)
df.drop(df.loc[df['YCORD'] == 0].index, inplace=True)

lat, lon = utm.to_latlon(df["XCORD"], df["YCORD"], 24, "M")
df['Latitude'] = lat  # adição da latitude no DF
df['Longitude'] = lon  # adição da Longitude no DF
del(lat)
del(lon)


# === APAGANDO COLUNAS SEM USO === #
try:
    df = df.drop(['ANO', 'Hora_de_Criacao', 'FAIXA_3HS', 'FAIXA_6HS', 'Endereco', 'PONTO_REFERENCIA', 'Bairro',
              'GRANDE_ARACAJU', 'Cod._Tipo', 'Descricao', 'DESC_COM_SUB_TIPO', 'DESC_SINESP', 'Cod._Sub_Tipo',
              'Batalhao', 'AISP', 'CMD', 'GRUPO_FINALIZACAO',
              'TIPO_ATENDIMENTO', 'SITUACAO_SENASP', 'Cod._Final.', 'Obs._Finalizacao',
              'Solicitante', 'Telefone', 'Despachado', 'Tempo_Despacho', 'Chegada_Local', 'Tempo_Deslocamento',
              'Placa', 'TEMPO_ATENDIMENTO'], axis=1)
except Exception as erro:
    print(f'Ocorreu um erro ao apagar as colunas do df - {erro}')
    pass
print(f'Tempo para ajustar o BD (retirando NaN e inserindo colunas novas - {time.time() - t1}')

# === CRIAÇÃO DO LAYOUT DA APLICAÇÃO === #

app.layout = dbc.Container(
    [
            html.Div(
                    [
                        dbc.Row([
                            dbc.Col([
                                ThemeSwitchAIO(aio_id="theme", themes=[url_theme1, url_theme2], ),
                                html.H3('CEAC', style={'textAlign': 'center', 'margin':'15px'}),
                                # html.P('Projeto Dash_Py 0.7', className="text-success"),

                                html.H5('Registros',style={'textAlign': 'center',
                                           #'color': 'white'
                                                           'margin':'15px' }),

                                html.Div(id='total_acc'),

                                html.H6('OPM da área',style={'textAlign': 'left', 'margin': '15px'}),

                                dcc.Checklist(options={
                                        '1BPM': '1BPM',
                                        '5BPM': '5BPM',
                                        '8BPM': '8BPM',
                                        'BPTUR': 'BPTUR',
                                        '1CIPM': '1CIPM',
                                        '2CIPM': '2CIPM',
                                        '3CIPM': '3CIPM',
                                        '6CIPM': '6CIPM',
                                    },value=['1BPM', '5BPM', '8BPM', 'BPTUR',
                                           '1CIPM', '2CIPM', '3CIPM','6CIPM'], id='sel_opm',inputStyle={"margin-right": "10px",
                                                "margin-left": "10px"}),

                                html.H6('Cia da área', style={'textAlign': 'left', 'margin': '15px'}),
                                dcc.Dropdown(cias, ['TODAS'], id='sel_cias', placeholder="Selecione as Companhias..",
                                             style={'dropdown-content': '{padding: 8px}'}, multi=True),

                                html.H6('Municípios', style={'textAlign': 'left', 'margin': '15px'}),
                                dcc.Dropdown(municip,['TODOS'],id='sel_mun',placeholder="Selecione municípios...",
                                             style={'dropdown-content': '{padding: 8px}'},multi=True),

                                html.H6('Localidades', style={'textAlign': 'left', 'margin': '15px'}),
                                dcc.Dropdown(bairros,['TODOS'],id='sel_bairros',
                                             placeholder="Selecione a localidade...",
                                             style={'dropdown-content': '{padding: 8px}'},multi=True),

                                html.H6('Tipo de crime',style={'textAlign': 'left', 'margin': '15px'}),

                                dcc.Dropdown(tipos_descricao,
                                             ['ROUBO','FURTO', 'HOMICIDIO'],id='sel_descricao',
                                             placeholder="Selecione tipos...",
                                             style={'dropdown-content':'{padding: 8px; font-size: 8px}'},multi=True ),

                                html.H6('Sub Tipo de crime',
                                        style={'textAlign': 'left', 'margin': '15px'}),

                                dcc.Dropdown(sub_tipos_descricao,
                                             ['TODOS'],id='sel_sub_tipo',
                                             placeholder="Selecione o sub tipos...",
                                             style={'dropdown-content': '{padding: 8px; font-size: 8px}'},
                                             multi=True),

                                html.H6('Tipo de finalização',
                                        style={'textAlign': 'left', 'margin': '15px'}),

                                dcc.Dropdown(tipos_finalizacao,
                                             ['TODOS'],
                                             id='sel_fim',
                                             placeholder="Selecione tipos...",
                                             style={'dropdown-content': '{padding: 8px; font-size: 8px}'},
                                             multi=True),

                                html.H6('Faixa de horário',
                                        style={'textAlign': 'left', 'margin': '15px'}),

                                dcc.RangeSlider(0, 23, 1, marks=None,  value=[0, 23], id='faixa_horario',
                                                tooltip={"placement": "bottom", "always_visible": True}),


                                dcc.Checklist(['Inverso do intervalo'],[], id='inverso',
                                                style={"color": "red"},inputStyle={"margin-right": "10px",
                                                "margin-left": "10px"}),

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
                                        value=['SEGUNDA','TERCA','QUARTA','QUINTA',
                                               'SEXTA','SABADO','DOMINGO'],id='dias_semana',
                                        inputStyle={"margin-right": "10px",
                                                    "margin-left": "10px"}
                                ),

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

                                html.H6('Busca no histórico',
                                        style={'textAlign': 'left', 'margin': '15px'}),

                                dcc.Input(
                                    placeholder='Digite aqui...',
                                    type='text',
                                    value='',
                                    id='sel_historico'),
                        ], md=2),

                            dbc.Col([
                                html.H1(children='Acionamentos 190', style={'textAlign': 'center'}),
                                html.Br(),
                                dbc.Row([
                                    dbc.Col([dcc.Graph(id='gra_mes')], md=6),
                                    dbc.Col([dcc.Graph(id='gra_opm')], md=6),
                                ]),
                                html.Br(),
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
                            ]) # LINHA MESTRE
            ]) # DIV MESTRE
    ],
    fluid=True,
    className="dbc"
)


# === CRIAÇÃO DAS FUNÇÕES E CALLBACK === #
@app.callback(
    [
    Output('gra_mes','figure'),
    Output('gra_opm','figure'),
    Output('gra_turno', 'figure'),
    Output('gra_fim','figure'),
    Output('gra_mun', 'figure'),
    Output('total_acc','children'),
    Output('gra_tipo','figure'),
    Output('gra_mapa', 'figure'),
    Output('gra_localidade', 'figure'),

    # Output('tbl_out', 'children')
    # Output('gra_radar', 'figure')
    ],

    [
        Input('sel_mun','value'),
        Input('sel_descricao', 'value'),
        Input('sel_historico', 'value'),
        Input('janela_tempo', 'start_date'),
        Input('janela_tempo', 'end_date'),
        Input('faixa_horario','value'),
        Input('dias_semana','value'),
        Input('sel_fim','value'),
        Input('sel_opm','value'),
        Input('sel_bairros', 'value'),
        Input('sel_sub_tipo','value'),
        Input(ThemeSwitchAIO.ids.switch("theme"), "value"),
        Input('inverso','value'),
        Input('sel_cias','value')

    ])
def atualizar(mun, crime, historico,dataI, dataF, faixa_hora,
              dias_semana, selecao_finalizacao, opm, bairro_local, sub_tipo, toggle, inverso_intervalo, cias_sel):

    template = template_theme1 if toggle else template_theme2
    ti_alteracao = time.time()
    mask = (df['Novo_tempo2'] >= dataI) & (df['Novo_tempo2'] <= dataF)
    df_filtro = df.loc[mask]
    if len(inverso_intervalo)>0:
        print('Inverso ativado')
        mask = (df_filtro['Hora_int'] < faixa_hora[0]) | (df_filtro['Hora_int'] > faixa_hora[1])
    else:
        mask = (df_filtro['Hora_int'] >= faixa_hora[0]) & (df_filtro['Hora_int'] <= faixa_hora[1])
    df_filtro = df_filtro.loc[mask]
    # print(crime)
    # print(historico)
    historico = historico.replace(' ','')
    lista_historico = historico.split(',')
    del(historico)
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

    # -----------------------------------------------------------------------------------
    # df_tempo_medio = df_filtro.groupby(['Intervalo_aberta_fechada', 'Hora_int_textual'])[['XCORD']].apply(op).reset_index()
    # df_tempo_medio.columns = ['Qtd minutos aberta', 'Hora da ligação','Qtd']
    df_cidades = df_filtro['Municipio'].value_counts().to_frame().reset_index()
    df_cidades.columns = ['Municipio', 'Qtd']
    df_tipo = df_filtro['DESCRICAO_OK'].value_counts().to_frame().reset_index()
    df_tipo.columns = ['Tipo', 'Qtd']
    df_datas = df_filtro['Data_de_Criacao'].value_counts().to_frame().reset_index()
    df_datas.columns = ['Data', 'Qtd']
    df_fim = df_filtro['Descricao_Finalizacao'].value_counts().to_frame().reset_index()
    df_fim.columns = ['Finalização', 'Qtd']
    df_mes = df_filtro.groupby(['Municipio','MES'])[['XCORD']].apply(op).reset_index()
    df_mes.columns = ['Municipio', 'Mes','Qtd']
    df_turnos = df_filtro['TURNOS'].value_counts().to_frame().reset_index()
    df_turnos.columns = ['Turno','Qtd']
    df_opm = df_filtro.groupby(['Municipio','BPM_NOVO'])[['XCORD']].apply(op).reset_index()
    df_opm.columns = ['Municipio', 'OPM','Qtd']
    df_localidade = df_filtro['BAIRRO_NOVO'].value_counts().to_frame().reset_index()
    df_localidade.columns = ['Localidade','Qtd']

    total_190 = len(df_filtro.index)
    total_geral = len(df.index)

    total_acionamentos = [html.P('{0:,.0f}'.format(total_190),
                       style={'textAlign': 'center',
                              'color': 'orange',
                              'fontSize': 40}),

                          html.P(
                                str(round((total_190/total_geral)*100,2)) + '% de '
                               + '{0:,.0f}'.format(total_geral)
                                 + ' protocolos',
                                 style={
                                     'textAlign': 'center',
                                     'color': 'green',
                                     'fontSize': 15,
                                     'margin-top': '-18px'})
                          ]

    #tabela = dash_table.DataTable(df_mes.to_dict('records'),[{"name": i, "id": i} for i in df_mes.columns], id='tbl'),

    fig1 = px.bar(df_mes, x='Mes', y='Qtd', color='Municipio', barmode='group',
                  category_orders={"Mes": ["JANEIRO", "FEVEREIRO", "MARCO", "ABRIL", "MAIO"]}, title="Serie histórica")

    fig2 = px.pie(df_opm, values='Qtd', names='OPM', hole=.3, title="OPM")

    fig3 = px.bar(df_turnos, x='Turno', y='Qtd', category_orders={"Turno": ["1TURNO", "2TURNO", "3TURNO", "4TURNO"]},
                  text='Qtd',title="Turnos")

    fig4 = px.bar(df_fim, x= 'Finalização', y='Qtd', orientation='v', title="Finalizações",  text='Qtd')

    fig5 = px.bar(df_cidades, x="Municipio", y='Qtd',title="Municípios",  text='Qtd')

    fig6 = px.pie(df_tipo, values='Qtd', names='Tipo', hole=0.3 , title="Tipo")

    fig7 = px.density_mapbox(df_filtro, lat='Latitude', lon='Longitude', z='Peso_crimes' ,radius=70,
                            center=dict(lat=-10.9, lon=-37.06), zoom=10, hover_name="DESCRICAO_OK",
                            hover_data={'Latitude':False, 'Longitude':False, 'Peso_crimes':False,
                                        'Ocorrencia':True,
                                        'Data':True, 'Hora':True,
                                        'Cia':True, 'Viatura':True
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

    fig8 = px.bar(df_localidade, x="Localidade", y='Qtd',title="Localidades",  text='Qtd')

    # fig8 = px.line_polar(df_tempo_medio, r='Qtd minutos aberta', theta='Hora da ligação', line_close=True)

    # fig_teste = px.scatter_mapbox(df_filtro, lat="Latitude", lon="Longitude", center=dict(lat=-10.9, lon=-37.06),
    #                               zoom=10, mapbox_style="open-street-map", height=900)
    # fig_teste.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    #####################################################



    # === ATUALIZAÇÃO DAS FIGURAS === #

    fig1.update_layout(margin=dict(l=10, r=10, t=40, b=10),height = 250, template = template,
                       yaxis_title=None, xaxis_title=None)
    fig2.update_layout(margin=dict(l=10, r=10, t=40, b=10),height = 250, template = template,
                       yaxis_title=None, xaxis_title=None)
    fig3.update_layout(margin=dict(l=10, r=10, t=40, b=10),height = 250, template = template,
                       yaxis_title=None, xaxis_title=None)
    fig4.update_layout(margin=dict(l=10, r=10, t=40, b=10),height = 250, template = template,
                       uniformtext_minsize=6, uniformtext_mode='hide',yaxis_title=None, xaxis_title=None)
    fig5.update_layout(margin=dict(l=10, r=10, t=40, b=10),height = 300, template = template,
                       uniformtext_minsize=6, uniformtext_mode='hide',yaxis_title=None, xaxis_title=None)
    fig6.update_traces(textposition='inside')
    fig6.update_layout(margin=dict(l=10, r=10, t=40, b=10),height = 300, template = template,
                       uniformtext_minsize=8, uniformtext_mode='hide', yaxis_title=None, xaxis_title=None)
    fig7.update_layout(margin=dict(l=10, r=10, t=40, b=10),height = 900)
    fig8.update_layout(margin=dict(l=10, r=10, t=40, b=10),height = 300, template = template,
                       yaxis_title=None, xaxis_title=None)

    # fig8.update_traces(fill='toself')
    # fig8.update_layout(margin=dict(l=10, r=10, t=40, b=10),height = 900, template = 'plotly_dark')

    print(f'Tempo para Atualizar o BD (após cada manipulação) - {time.time() - ti_alteracao}')

    del template, mask, df_filtro, df_mes, df_datas, df_fim, df_opm, df_cidades, df_turnos, df_localidade, df_tipo, op, lista_historico
    return fig1 ,fig2, fig3, fig4, fig5, total_acionamentos, fig6, fig7 , fig8 #, tabela

def main():
    app.run_server(debug=False)


# === INICIALIZANDO A FUNÇÃO  main() === #

if __name__ == '__main__':
    main()
    # app.run_server(debug=True) # local
    # app.run_server(port=8051,debug=True)



