from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

import os
from dotenv import load_dotenv
import smtplib

load_dotenv()

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

# from_addr = input('From: ')
# password = input('Password: ')
# to_addr = input('To: ')
# smtp_server = input('SMTP server: ')

from_addr = os.environ.get('ENV_EMLADDR')
password = os.environ.get('ENV_EMLPAW')
to_addr = os.environ.get('ENV_EMLNOTION2')
smtp_server = "smtp.mxhichina.com"

msg = MIMEText('来自小悠的通知', 'plain', 'utf-8')
msg['From'] = _format_addr('小悠 <%s>' % from_addr)
msg['To'] = _format_addr('管理员 <%s>' % to_addr)
msg['Subject'] = Header(f'叮！{to_addr}', 'utf-8').encode()

smtp_port = 587
server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()
