import os
from dash import Dash, html, dcc, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import time
import sqlite3
from sqlalchemy import Table, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_manager, UserMixin, LoginManager
import utm
import psycopg2

template_theme1 = "bootstrap"
template_theme2 = "cyborg"  # "darkly"
url_theme1 = dbc.themes.BOOTSTRAP
url_theme2 = dbc.themes.CYBORG

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

t1 = time.time()


# TODO: Retirar esses @profile
def pesos_crime(row):
    if row['SITUACAO_SENASP'] == 'CVLI':
        return 80
    elif row['SITUACAO_SENASP'] == 'CVNLI':
        return 20
    elif row['SITUACAO_SENASP'] == 'CVP':
        return 15
    elif row['SITUACAO_SENASP'] == 'CNVP':
        return 5
    elif row['SITUACAO_SENASP'] == 'CVNP':
        return 5
    return 1


def hora_int(row):
    if row['FAIXA_HORARIA'] == '00:00':
        return 0
    elif row['FAIXA_HORARIA'] == '01:00':
        return 1
    elif row['FAIXA_HORARIA'] == '02:00':
        return 2
    elif row['FAIXA_HORARIA'] == '03:00':
        return 3
    elif row['FAIXA_HORARIA'] == '04:00':
        return 4
    elif row['FAIXA_HORARIA'] == '05:00':
        return 5
    elif row['FAIXA_HORARIA'] == '06:00':
        return 6
    elif row['FAIXA_HORARIA'] == '07:00':
        return 7
    elif row['FAIXA_HORARIA'] == '08:00':
        return 8
    elif row['FAIXA_HORARIA'] == '09:00':
        return 9
    elif row['FAIXA_HORARIA'] == '10:00':
        return 10
    elif row['FAIXA_HORARIA'] == '11:00':
        return 11
    elif row['FAIXA_HORARIA'] == '12:00':
        return 12
    elif row['FAIXA_HORARIA'] == '13:00':
        return 13
    elif row['FAIXA_HORARIA'] == '14:00':
        return 14
    elif row['FAIXA_HORARIA'] == '15:00':
        return 15
    elif row['FAIXA_HORARIA'] == '16:00':
        return 16
    elif row['FAIXA_HORARIA'] == '17:00':
        return 17
    elif row['FAIXA_HORARIA'] == '18:00':
        return 18
    elif row['FAIXA_HORARIA'] == '19:00':
        return 19
    elif row['FAIXA_HORARIA'] == '20:00':
        return 20
    elif row['FAIXA_HORARIA'] == '21:00':
        return 21
    elif row['FAIXA_HORARIA'] == '22:00':
        return 22
    return 23


# === CRIAÇÃO DE VARIÁVEIS DO SISTEMA === #


df = pd.read_excel('base.xlsx')  # mudar entre base_teste.xlsx e base.xlsx
print(f'Tempo para ler o BD - {time.time() - t1}')
df.drop(df.loc[df['Fechado'] == '// ::'].index, inplace=True)
df.drop(df.loc[df['GRUPO_FINALIZACAO'] == '4.NAO_ENTRA_NA_ESTATISTICA'].index, inplace=True)

municip = ['TODOS', 'ARACAJU', 'NOSSA SENHORA DO SOCORRO', 'BARRA DOS COQUEIROS',
           'SAO CRISTOVAO', 'MARUIM', 'LARANJEIRAS',
           'RIACHUELO', 'SANTO AMARO DAS BROTAS', 'DIVINA PASTORA']
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
del cleanedList

bairros = list(set(df['BAIRRO_NOVO'].to_list()))
bairros.append('TODOS')
cias_temp = []
df['Cia'] = df['CIA_NOVA']
cias = list(set(df['Cia'].to_list()))
cleanedList = [x for x in cias if str(x) != 'nan']
cias = cleanedList
del cleanedList
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
del lat
del lon

# === APAGANDO COLUNAS SEM USO === #
try:
    lista_colunas = ['ANO', 'Hora_de_Criacao', 'FAIXA_3HS', 'Endereco', 'PONTO_REFERENCIA', 'Bairro',
                     'GRANDE_ARACAJU', 'Cod._Tipo', 'Descricao', 'DESC_COM_SUB_TIPO', 'DESC_SINESP', 'Cod._Sub_Tipo',
                     'Batalhao', 'AISP', 'CMD', 'GRUPO_FINALIZACAO',
                     'TIPO_ATENDIMENTO', 'SITUACAO_SENASP', 'Cod._Final.', 'Obs._Finalizacao',
                     'Solicitante', 'Telefone', 'Despachado', 'Tempo_Despacho', 'Chegada_Local', 'Tempo_Deslocamento',
                     'Placa', 'TEMPO_ATENDIMENTO']
    for coluna in lista_colunas:
        try:
            df = df.drop([coluna], axis=1)
            print(f'Drop realizado na coluna {coluna}')
        except:
            print(f'A coluna {coluna} não pode ser excluída')
            pass
except Exception as erro:
    print(f'Ocorreu um erro ao apagar as colunas do df - {erro}')
    pass
print(f'Tempo para ajustar o BD (retirando NaN e inserindo colunas novas - {time.time() - t1}')


# === CONECTANDO AO BANCO SQL === #

# conn = sqlite3.connect('data.sqlite')
# engine = create_engine('sqlite:///data.sqlite')

conn = psycopg2.connect(host='ec2-3-210-173-88.compute-1.amazonaws.com', database='d15949k84tt69d',
                        user='evgdmltwwnjdfn',
                        password='f3623d6aae90a95d478cc153c816846d9d615c3ca60385e536f76e56a175dca0')

engine = create_engine(
    'postgresql://evgdmltwwnjdfn:f3623d6aae90a95d478cc153c816846d9d615c3ca60385e536f76e56a175dca0@ec2' \
      '-3-210-173-88.compute-1.amazonaws.com:5432/d15949k84tt69d')



db = SQLAlchemy()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_cpf = db.Column(db.String(11), unique=True, nullable=False)
    user_name = db.Column(db.String(60), unique=True, nullable=False)
    user_password = db.Column(db.String(60), nullable=False)
    user_email = db.Column(db.String(60), unique=True, nullable=False)
    user_aprovado = db.Column(db.String(1))


User_table = Table('users', Users.metadata)

########################################

app2 = Dash(__name__, external_stylesheets=[url_theme2, dbc_css])
server = app2.server
app2.config.suppress_callback_exceptions = True
######################################

server.config.update(
    SECRET_KEY=os.urandom(12),
    SQLALCHEMY_DATABASE_URI= 'postgresql://evgdmltwwnjdfn:f3623d6aae90a95d478cc153c816846d9d615c3ca60385e536f76e56a175d'
                             'ca0@ec2-3-210-173-88.compute-1.amazonaws.com:5432/d15949k84tt69d',
    SQLALCHEMY_TRACK_MODIFICATIONS=False)     # TODO: FAZER A MUDANÇA PARA O BANCO SQL

db.init_app(server)


class Users(UserMixin, Users):
    pass
