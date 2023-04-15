import smtplib
import ssl

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# def enviar(nome, cod, destino):
#     ctx = ssl.create_default_context()
#     password = "gsfufrphfzhybemi"    # Your app password goes here
#     sender = "cpmc.ceac@gmail.com"    # Your e-mail address
#     receiver = destino  # Recipient's address
#     message = f"""
#     Ola {nome},
#     Consta em nossos sistemas uma solicitacao de mudanca de senha da plataforma do CEAC-DASH.
#     esse sera seu codigo de validacao (composto por 4 numeros) para mudar a senha do CEAC-DASH ->  {cod}
#     """
#     with smtplib.SMTP_SSL("smtp.gmail.com", port=465, context=ctx) as server:
#         server.login(sender, password)
#         server.sendmail(sender, receiver, message,)


def enviar(nome, cod, destino):

    # Define the transport variables
    ctx = ssl.create_default_context()
    password = "gsfufrphfzhybemi"    # Your app password goes here
    sender = "cpmc.ceac@gmail.com"    # Your e-mail address
    receiver = destino  # Recipient's address

    # Create the message
    message = MIMEMultipart("alternative")
    message["Subject"] = "Código de validação do painel do CEAC/CPMC"
    message["From"] = sender
    message["To"] = receiver

    # HTML version
    # html = """\
    # <html>
    #   <body>
    #     <p>
    #         <i>Hello</i>
    #         <u>from</u>
    #         <b>Python</b>.
    #     </p>
    #     <p>
    #         Try out the APIs at
    #         <a href="https://www.abstractapi.com/">Abstract API</a>.
    #     </p>
    #   </body>
    # </html>
    # """

    # Plain text alternative version
    plain = f"""\
    Olá {nome},
    
    Consta em nossos sistemas uma solicitação de mudança de senha da plataforma do CEAC-DASH.
    Caso tenha sido você a solicitar tal procedimento, estamos enviando um código com validade de 30 minutos.
    Logo abaixo é apresentado o código de validação (composto por 4 números) para mudar a senha do nosso sistema:

    {cod}
    
    Atenciosamente,
    
    CEAC / CPMC.
    """

    # Add the different alternative parts in order of increasing complexity
    # starting with the simplest first, i.e. the plain text version first.
    message.attach(MIMEText(plain, "plain"))
    # message.attach(MIMEText(html, "html"))

    # Connect with server and send the message
    with smtplib.SMTP_SSL("smtp.gmail.com", port=465, context=ctx) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, message.as_string())
