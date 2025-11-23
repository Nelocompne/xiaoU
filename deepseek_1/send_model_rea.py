from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

import os
import sys
from dotenv import load_dotenv
import smtplib

# 添加当前目录到Python路径，以便导入readft模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

# 尝试导入readft模块
try:
    from readft import read_boot_time_custom
    can_import_readft = True
except ImportError:
    can_import_readft = False
    print("警告: 无法导入readft模块，将使用简化版开机时间读取")

def get_boot_time_info():
    """
    获取开机时间信息
    """
    if can_import_readft:
        # 使用readft模块的函数
        result = read_boot_time_custom("%Y-%m-%d %H:%M:%S")
        if result:
            return f"""
系统开机信息:
----------------------------
开机时间: {result['boot_time'].strftime('%Y-%m-%d %H:%M:%S')}
运行时长: {result['uptime_str']}
当前时间: {result['current_time'].strftime('%Y-%m-%d %H:%M:%S')}
----------------------------
"""
        else:
            return "错误: 无法获取开机时间信息"
    else:
        # 简化版开机时间读取
        try:
            import json
            from datetime import datetime
            
            with open("str/date.json", 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            boot_time_str = data["boot_time"]
            boot_time = datetime.fromisoformat(boot_time_str)
            current_time = datetime.now()
            uptime = current_time - boot_time
            
            return f"""
系统开机信息:
----------------------------
开机时间: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}
运行时长: {str(uptime).split('.')[0]}
当前时间: {current_time.strftime('%Y-%m-%d %H:%M:%S')}
----------------------------
"""
        except Exception as e:
            return f"错误: 无法读取开机时间 - {e}"

from_addr = os.environ.get('ENV_EMLADDR')
password = os.environ.get('ENV_EMLPAW')
to_addr = os.environ.get('ENV_EMLNOTION2')
smtp_server = "smtp.mxhichina.com"

# 获取开机时间信息
boot_time_info = get_boot_time_info()

# 创建邮件内容
email_content = f"""
来自小悠的系统通知

{boot_time_info}

此邮件由系统自动发送，请勿回复。
"""

msg = MIMEText(email_content, 'plain', 'utf-8')
msg['From'] = _format_addr('小悠 <%s>' % from_addr)
msg['To'] = _format_addr('管理员 <%s>' % to_addr)

# 在主题中添加开机时间信息
msg['Subject'] = Header(f'系统状态通知 - 开机时间已记录 测试', 'utf-8').encode()

smtp_port = 587
server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()

print("邮件发送成功！")