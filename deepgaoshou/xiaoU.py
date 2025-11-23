#!/usr/bin/env python3
"""
小悠系统监控主程序
功能：
1. 首次联网成功后发送上线通知
2. 持续监控网络状态，断网重连后发送重新联网通知
3. 持续监控磁盘空间，空间不足时发送警告（每180分钟一次）
"""

import time
import platform
from datetime import datetime, timedelta
import internet_check
import system_uptime
import disk_usage
import email_sender
from email_composer import email_composer

class XiaoUSystem:
    def __init__(self):
        self.online_notification_sent = False
        self.reconnect_notification_sent = False
        self.last_network_status = None  # 记录上一次网络状态
        self.last_disk_warning_time = None
        self.disk_check_interval = 300  # 磁盘检查间隔（秒）
        self.network_check_interval = 10  # 网络检查间隔（秒）
        
        # 根据操作系统设置默认挂载点
        if platform.system() == "Windows":
            self.mount_point = "C:\\"
        else:
            self.mount_point = "/"
        
        print(f"系统类型: {platform.system()}")
        print(f"监控的挂载点: {self.mount_point}")
        
    def run_online_check(self):
        """执行联网检测和上线通知"""
        print("开始检测网络连接...")
        
        while not self.online_notification_sent:
            current_status = internet_check.check_internet_connection()
            
            # 记录初始网络状态
            if self.last_network_status is None:
                self.last_network_status = current_status
            
            if current_status:
                print("检测到网络连接成功！")
                
                # 获取系统信息
                boot_time, uptime = system_uptime.get_system_uptime()
                
                # 编写邮件内容
                title = email_composer.format_title("小悠上线提醒")
                content = email_composer.compose_online_notification(boot_time, uptime)
                
                # 发送邮件
                if email_sender.send_email(title, content):
                    self.online_notification_sent = True
                    self.reconnect_notification_sent = False  # 重置重新联网通知状态
                    print("上线通知邮件发送成功！")
                else:
                    print("上线通知邮件发送失败，将在下次检测时重试")
            
            # 更新网络状态
            self.last_network_status = current_status
            
            # 等待5秒后再次检测
            time.sleep(5)
    
    def run_network_monitor(self):
        """持续监控网络状态，检测断网重连情况"""
        print("开始持续网络状态监控...")
        
        while True:
            try:
                current_status = internet_check.check_internet_connection()
                
                # 检测网络状态变化：从断网到联网
                if (self.last_network_status is not None and 
                    not self.last_network_status and 
                    current_status and 
                    self.online_notification_sent and
                    not self.reconnect_notification_sent):
                    
                    print("检测到网络重新连接！")
                    
                    # 编写邮件内容
                    title = email_composer.format_title("小悠已重新联网")
                    content = email_composer.compose_reconnect_notification()
                    
                    # 发送邮件
                    if email_sender.send_email(title, content):
                        self.reconnect_notification_sent = True
                        print("重新联网通知邮件发送成功！")
                    else:
                        print("重新联网通知邮件发送失败")
                
                # 如果网络断开，重置重新联网通知状态
                if not current_status and self.reconnect_notification_sent:
                    self.reconnect_notification_sent = False
                    print("网络连接已断开")
                
                # 更新网络状态
                self.last_network_status = current_status
                
            except Exception as e:
                print(f"网络状态监控出错: {e}")
            
            # 等待指定间隔后再次检查
            time.sleep(self.network_check_interval)
    
    def run_disk_monitor(self):
        """执行磁盘空间监控"""
        print("开始磁盘空间监控...")
        
        while True:
            try:
                # 检查磁盘使用情况
                total_gb, used_gb, free_gb, percent = disk_usage.check_disk_usage(self.mount_point)
                
                # 如果获取数据失败，跳过本次检查
                if total_gb == 0 and used_gb == 0 and free_gb == 0:
                    print("无法获取磁盘使用信息，等待下次检查...")
                    time.sleep(self.disk_check_interval)
                    continue
                
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
                else:
                    print("磁盘空间充足")
                
            except Exception as e:
                print(f"磁盘监控出错: {e}")
            
            # 等待指定间隔后再次检查
            time.sleep(self.disk_check_interval)
    
    def run(self):
        """主运行函数"""
        print("小悠系统监控启动中...")
        print("=" * 50)
        
        # 显示系统信息
        print(f"操作系统: {platform.system()} {platform.release()}")
        print(f"Python版本: {platform.python_version()}")
        
        # 启动联网检测（阻塞，直到首次联网成功发送通知）
        self.run_online_check()
        
        print("=" * 50)
        print("上线通知已完成，开始持续网络和磁盘监控...")
        
        # 启动网络状态监控（持续运行）
        # 注意：由于Python的GIL限制，这里使用简单的循环而非真正的并行
        # 在实际应用中，可以考虑使用多线程或异步编程
        try:
            while True:
                # 运行网络监控
                self.run_network_monitor()
                
                # 运行磁盘监控
                self.run_disk_monitor()
                
                # 短暂休眠避免过度占用CPU
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("程序被用户中断")
        except Exception as e:
            print(f"程序运行出错: {e}")

if __name__ == "__main__":
    xiao_u = XiaoUSystem()
    xiao_u.run()