# import sqlite3
# import pandas as pd
import datetime
import pygsheets


def registrar(nome, cpf, email):
    dt_agora = datetime.datetime.utcnow() + datetime.timedelta(hours=-3)
    agora = dt_agora.strftime('%d/%m/%Y - %H:%M:%S')

    dados = [cpf, nome, email, agora, 'Entrada']
    client = pygsheets.authorize(
        client_secret='client_secret_640793899938-gmj6mrgve57e9m79ir5i5tp258dsl9kt.'
                      'apps.googleusercontent.com.json')
    sh = client.open('Python_projetos')
    wks = sh.worksheet('title', '23 - Logs')
    wks.add_rows(1)
    linhas = len(wks.get_col(1))
    wks.update_row(linhas, dados)

'''
    conn2 = sqlite3.connect('acessos.sqlite')
    cursor_login = conn2.cursor()

    #
    # # criando a tabela (schema)
    # cursor_log.execute("""
    # CREATE TABLE logs (
    #         id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    #         nome TEXT NOT NULL,
    #         cpf    VARCHAR(11) NOT NULL,
    #         email TEXT NOT NULL,
    #         acessado_em DATE NOT NULL
    #         tipo TEXT NOT NULL,
    # );
    # """)
    # print('Tabela criada com sucesso.')

    dados_login_limpos = ""
    dados_login = [nome, cpf, email, agora, 'Entrada']
    # inserindo dados na tabela
    dados_login_limpos = dados_login_limpos + repr(dados_login[0])
    dados_login_limpos = dados_login_limpos + ', '
    dados_login_limpos = dados_login_limpos + repr(dados_login[1])
    dados_login_limpos = dados_login_limpos + ', '
    dados_login_limpos = dados_login_limpos + repr(dados_login[2])
    dados_login_limpos = dados_login_limpos + ', '
    dados_login_limpos = dados_login_limpos + repr(dados_login[3])
    dados_login_limpos = dados_login_limpos + ', '
    dados_login_limpos = dados_login_limpos + repr(dados_login[4])

    cursor_login.execute(f"""
    INSERT INTO logs (nome, cpf, email, acessado_em, tipo)
    VALUES ({dados_login_limpos})
    """)

    # gravando no bd
    conn2.commit()

    print('Dados inseridos com sucesso.')

    # lendo os dados
    # cursor_login.execute("""
    # SELECT * FROM logs;
    # """)
    #
    # for linha in cursor_log.fetchall():
    #     print(linha)
    #

    df = pd.read_sql('select * from logs', conn2)
    print('O Banco de dados de acesso ficou assim')
    print(df[['id', 'cpf', 'nome', 'acessado_em', 'tipo']])

    # desconectando...
    conn2.close()
'''

