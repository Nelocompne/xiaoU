from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

import os
import sys
from dotenv import load_dotenv
import smtplib
from datetime import datetime

# 添加当前目录到Python路径，以便导入readft模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

# 导入readft模块
try:
    from readft import read_boot_time_custom
    can_import_readft = True
    print("成功导入readft模块")
except ImportError as e:
    can_import_readft = False
    print(f"警告: 无法导入readft模块 - {e}")
    print("将使用内置的开机时间读取功能")

def get_boot_time_info():
    """
    获取开机时间信息
    """
    if can_import_readft:
        # 使用readft模块的函数
        try:
            result = read_boot_time_custom("%Y-%m-%d %H:%M:%S")
            if result:
                return f"""
系统开机信息:
----------------------------
📅 开机时间: {result['boot_time'].strftime('%Y-%m-%d %H:%M:%S')}
⏱️ 运行时长: {result['uptime_str']}
🕐 当前时间: {result['current_time'].strftime('%Y-%m-%d %H:%M:%S')}
----------------------------
"""
            else:
                return "错误: 无法获取开机时间信息"
        except Exception as e:
            return f"调用readft模块时出错: {e}"
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
            
            # 计算运行时间的各个部分
            days = uptime.days
            hours, remainder = divmod(uptime.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            # 构建运行时间字符串
            uptime_parts = []
            if days > 0:
                uptime_parts.append(f"{days}天")
            if hours > 0:
                uptime_parts.append(f"{hours}小时")
            if minutes > 0:
                uptime_parts.append(f"{minutes}分钟")
            if seconds > 0 or not uptime_parts:
                uptime_parts.append(f"{seconds}秒")
            
            uptime_str = "".join(uptime_parts)
            
            return f"""
系统开机信息:
----------------------------
开机时间: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}
运行时长: {uptime_str}
当前时间: {current_time.strftime('%Y-%m-%d %H:%M:%S')}
----------------------------
"""
        except Exception as e:
            return f"错误: 无法读取开机时间 - {e}"

def get_system_uptime_days():
    """
    获取系统运行天数（用于邮件标题）
    """
    try:
        with open("time/date.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
        boot_time = datetime.fromisoformat(data["boot_time"])
        uptime_days = (datetime.now() - boot_time).days
        return uptime_days
    except:
        return None

from_addr = os.environ.get('ENV_EMLADDR')
password = os.environ.get('ENV_EMLPAW')
to_addr = os.environ.get('ENV_EMLNOTION2')
smtp_server = "smtp.mxhichina.com"

# 获取当前时间（脚本启动时间）
script_start_time = datetime.now()
start_time_formatted = script_start_time.strftime("%Y-%m-%d %H:%M:%S")

# 获取开机时间信息
boot_time_info = get_boot_time_info()

# 获取系统运行天数
uptime_days = get_system_uptime_days()

# 创建邮件内容
email_content = f"""
来自小悠的系统通知

脚本启动时间: {start_time_formatted}

{boot_time_info}

此邮件由系统自动发送，请勿回复。
"""

msg = MIMEText(email_content, 'plain', 'utf-8')
msg['From'] = _format_addr('小悠 <%s>' % from_addr)
msg['To'] = _format_addr('管理员 <%s>' % to_addr)

# 在主题中使用更简洁的时间格式
short_time_format = script_start_time.strftime("%m-%d %H:%M")
msg['Subject'] = Header(f'系统状态报告 - {short_time_format}', 'utf-8').encode()

smtp_port = 587
server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()

print(f"邮件发送成功！发送时间: {start_time_formatted}")