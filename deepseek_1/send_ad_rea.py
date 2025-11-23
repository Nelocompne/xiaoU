from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

import os
import json
from dotenv import load_dotenv
import smtplib
from datetime import datetime

load_dotenv()

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def read_boot_time():
    """
    读取time/date.json文件中的boot_time值并格式化
    """
    file_path = "str/date.json"
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        return "错误: 未找到开机时间记录文件"
    
    try:
        # 读取JSON文件
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 获取boot_time值
        boot_time_str = data.get("boot_time")
        if not boot_time_str:
            return "错误: 未找到 boot_time 字段"
            
        # 解析时间
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
        
        # 格式化输出
        boot_time_formatted = boot_time.strftime("%Y-%m-%d %H:%M:%S")
        current_time_formatted = current_time.strftime("%Y-%m-%d %H:%M:%S")
        
        return f"""
系统开机信息:
----------------------------
开机时间: {boot_time_formatted}
运行时长: {uptime_str}
当前时间: {current_time_formatted}
----------------------------
"""
        
    except Exception as e:
        return f"读取开机时间时出错: {e}"

from_addr = os.environ.get('ENV_EMLADDR')
password = os.environ.get('ENV_EMLPAW')
to_addr = os.environ.get('ENV_EMLNOTION2')
smtp_server = "smtp.mxhichina.com"

# 读取开机时间信息
boot_time_info = read_boot_time()

# 创建邮件内容
email_content = f"""
来自小悠的系统通知

{boot_time_info}

此邮件由系统自动发送，请勿回复。
"""

msg = MIMEText(email_content, 'plain', 'utf-8')
msg['From'] = _format_addr('小悠 <%s>' % from_addr)
msg['To'] = _format_addr('管理员 <%s>' % to_addr)

# 在主题中添加开机时间
msg['Subject'] = Header(f'系统状态通知 - 开机时间已记录', 'utf-8').encode()

smtp_port = 587
server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()

print("邮件发送成功！")