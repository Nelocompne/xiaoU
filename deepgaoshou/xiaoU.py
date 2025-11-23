#!/usr/bin/env python3
"""
小悠系统监控主程序
功能：
1. 首次联网成功后发送上线通知
2. 持续监控磁盘空间，空间不足时发送警告（每180分钟一次）
"""

import time
from datetime import datetime, timedelta
import internet_check
import system_uptime
import disk_usage
import email_sender
from email_composer import email_composer

class XiaoUSystem:
    def __init__(self):
        self.online_notification_sent = False
        self.last_disk_warning_time = None
        self.disk_check_interval = 300  # 磁盘检查间隔（秒）
        self.mount_point = "/"  # 监控的挂载点，可根据需要修改
        
    def run_online_check(self):
        """执行联网检测和上线通知"""
        print("开始检测网络连接...")
        
        while not self.online_notification_sent:
            if internet_check.check_internet_connection():
                print("检测到网络连接成功！")
                
                # 获取系统信息
                boot_time, uptime = system_uptime.get_system_uptime()
                
                # 编写邮件内容
                title = email_composer.format_title("小悠上线提醒")
                content = email_composer.compose_online_notification(boot_time, uptime)
                
                # 发送邮件
                if email_sender.send_email(title, content):
                    self.online_notification_sent = True
                    print("上线通知邮件发送成功！")
                else:
                    print("上线通知邮件发送失败，将在下次检测时重试")
            
            # 等待5秒后再次检测
            time.sleep(5)
    
    def run_disk_monitor(self):
        """执行磁盘空间监控"""
        print("开始磁盘空间监控...")
        
        while True:
            try:
                # 检查磁盘使用情况
                total_gb, used_gb, free_gb, percent = disk_usage.check_disk_usage(self.mount_point)
                
                print(f"磁盘状态: {free_gb}GB 剩余 ({percent}% 已使用)")
                
                # 检查是否低于90GB阈值
                if free_gb < 90:
                    current_time = datetime.now()
                    
                    # 检查是否满足发送间隔（180分钟）
                    should_send = False
                    if self.last_disk_warning_time is None:
                        should_send = True
                    else:
                        time_diff = current_time - self.last_disk_warning_time
                        if time_diff >= timedelta(minutes=180):
                            should_send = True
                    
                    if should_send:
                        print("检测到磁盘空间不足，准备发送警告邮件...")
                        
                        # 编写邮件内容
                        title = email_composer.format_title("小悠提醒你空间不够了！")
                        content = email_composer.compose_disk_warning(
                            self.mount_point, total_gb, used_gb, free_gb, percent
                        )
                        
                        # 发送邮件
                        if email_sender.send_email(title, content):
                            self.last_disk_warning_time = current_time
                            print("磁盘空间警告邮件发送成功！")
                        else:
                            print("磁盘空间警告邮件发送失败")
                
            except Exception as e:
                print(f"磁盘监控出错: {e}")
            
            # 等待指定间隔后再次检查
            time.sleep(self.disk_check_interval)
    
    def run(self):
        """主运行函数"""
        print("小悠系统监控启动中...")
        print("=" * 50)
        
        # 启动联网检测（阻塞，直到首次联网成功发送通知）
        self.run_online_check()
        
        print("=" * 50)
        print("上线通知已完成，开始持续磁盘监控...")
        
        # 启动磁盘监控（持续运行）
        self.run_disk_monitor()

if __name__ == "__main__":
    xiao_u = XiaoUSystem()
    xiao_u.run()