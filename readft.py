import json
import os
from datetime import datetime

def read_boot_time_custom(format_str=None):
    """
    自定义格式读取开机时间
    
    Args:
        format_str: 时间格式化字符串，例如 "%Y-%m-%d %H:%M:%S"
    """
    if format_str is None:
        format_str = "%Y年%m月%d日 %H时%M分%S秒"
    
    try:
        # 读取JSON文件
        with open("str/date.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 获取boot_time
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
        
        # 输出结果
        print(f"📅 开机时间: {boot_time.strftime(format_str)}")
        print(f"⏱️  运行时长: {uptime_str}")
        print(f"🕐 当前时间: {current_time.strftime(format_str)}")
        
        return {
            "boot_time": boot_time,
            "current_time": current_time,
            "uptime": uptime,
            "uptime_str": uptime_str
        }
        
    except Exception as e:
        print(f"错误: {e}")
        return None

if __name__ == "__main__":
    # 使用默认格式
    read_boot_time_custom()
    
    print("\n" + "="*40 + "\n")
    
    # 使用自定义格式
    read_boot_time_custom("%Y-%m-%d %H:%M:%S")