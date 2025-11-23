import random
import time
from datetime import datetime, timedelta

class EmailComposer:
    def __init__(self):
        self.sent_titles = {}  # 存储已发送的标题和时间
        self.prefixes = [
            "哦齁齁❤", "啊齁齁❤", "齁唔❤", 
            "去了去了❤", "嗯？❤", "哇哦❤",
            "叮咚❤", "注意❤", "提醒❤"
        ]
    
    def _should_add_prefix(self, base_title):
        """
        检查是否需要在标题前添加随机前缀
        """
        current_time = datetime.now()
        
        if base_title in self.sent_titles:
            last_sent_time = self.sent_titles[base_title]
            # 检查是否在30分钟内
            if current_time - last_sent_time < timedelta(minutes=30):
                return True
        
        # 更新发送时间
        self.sent_titles[base_title] = current_time
        return False
    
    def format_title(self, base_title):
        """
        格式化邮件标题，确保30分钟内不重复
        """
        if self._should_add_prefix(base_title):
            prefix = random.choice(self.prefixes)
            return f"{prefix}{base_title}"
        else:
            return base_title
    
    def compose_online_notification(self, boot_time, uptime):
        """
        编写上线通知邮件内容
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        content = f"""小悠上线通知

系统状态报告：
• 当前时间：{current_time}
• 系统开机时间：{boot_time}
• 系统运行时间：{uptime}

系统已成功启动并连接到互联网。
小悠开始为您服务！❤

-- 自动发送于 {current_time}"""
        return content
    
    def compose_reconnect_notification(self):
        """
        编写重新联网通知邮件内容
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        content = f"""小悠重新联网通知

网络状态报告：
• 当前时间：{current_time}
• 事件：网络连接已恢复

系统检测到网络连接从断开状态恢复。
小悠继续为您服务！❤

-- 自动发送于 {current_time}"""
        return content
    
    def compose_disk_warning(self, mount_point, total_gb, used_gb, free_gb, percent):
        """
        编写磁盘空间警告邮件内容
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        content = f"""磁盘空间警告

系统检测到磁盘空间不足：
• 挂载点：{mount_point}
• 总空间：{total_gb} GB
• 已使用：{used_gb} GB ({percent}%)
• 剩余空间：{free_gb} GB

请注意及时清理磁盘空间，避免系统运行受到影响。

-- 自动发送于 {current_time}"""
        return content

# 全局实例
email_composer = EmailComposer()