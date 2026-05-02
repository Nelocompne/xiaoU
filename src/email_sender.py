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

def send_email(subject, content):
    """
    发送邮件
    subject: 邮件标题
    content: 邮件内容
    """
    try:
        from_addr = os.environ.get('ENV_EMLADDR')
        password = os.environ.get('ENV_EMLPAW')
        to_addr = os.environ.get('ENV_EMLNOTION2')
        smtp_server = "smtp.mxhichina.com"
        
        if not all([from_addr, password, to_addr]):
            print("错误: 邮件配置信息不完整")
            return False

        msg = MIMEText(content, 'plain', 'utf-8')
        msg['From'] = _format_addr(f'小悠 <{from_addr}>')
        msg['To'] = _format_addr(f'管理员 <{to_addr}>')
        msg['Subject'] = Header(subject, 'utf-8').encode()

        smtp_port = 587
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.set_debuglevel(0)  # 生产环境关闭调试
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()
        
        print(f"邮件发送成功: {subject}")
        return True
    except Exception as e:
        print(f"邮件发送失败: {e}")
        return False

if __name__ == "__main__":
    # 测试发送
    send_email("测试邮件", "这是一封测试邮件")