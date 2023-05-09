import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import sqlalchemy as sqlalchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

Base = automap_base()

engine = sqlalchemy.create_engine(
    "mysql+pymysql://saservice:mJ%40PcJ%21pNVs2%2AAW@10.51.11.183/sageservice?charset=utf8mb4")

msengine = sqlalchemy.create_engine(
    "mssql+pyodbc://saservice:mJ%40PcJ%21pNVs2%2AAW@10.52.11.50:1433/TSTDAT?driver=ODBC+Driver+17+for+SQL+Server")
metadata = MetaData()
metadata.reflect(msengine, only=['APPYM', 'APTCRO', 'ELVEND', 'APTCR'])
MS_Base = automap_base(metadata=metadata)
Base.prepare(autoload_with=engine)
MS_Base.prepare()

ms_session = Session(msengine, autoflush=False)
session = Session(engine)

elvend = MS_Base.classes.ELVEND
aptcro = MS_Base.classes.APTCRO
appym = MS_Base.classes.APPYM
aptcr = MS_Base.classes.APTCR
payments = Base.classes.payment_transaction


# payment_errors = Base.classes.emailRecord
# banklist = Base.classes.bankList

def get_ip_address(request):
    user_ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
    if user_ip_address:
        ip = user_ip_address.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def send_error_mail(resp_json):
    sender = 'mupumamgtsdev@gmail.com'
    receivers = 'seriterk@gmail.com'
    message = MIMEMultipart("alternative")
    message["Subject"] = "MUPUMA INFRATEL INTEGRATION API ERROR"
    message["From"] = sender
    message["To"] = receivers
    html = f"""\
                    <html>
                    <body>
                        <p>
                        Dear Team <br>
                        The following errorlist was returned while posting of an AP Payments Transaction <br>
                        {resp_json['errorList']['TEKESBERROR']} thus not allowing fullfilment of post requests to service "BNK9900", Kindly troubleshoot.<br>
                        Kind regards.
                        </p>
                    </body>
                    </html>
                    """
    msg = MIMEText(html, "html")
    password = "nnbhieknirlbtvcx"
    message.attach(msg)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(
            sender, receivers, message.as_string())


Login_Key = ""
Generate_otp_key = ""
Validate_otp_key = ""
