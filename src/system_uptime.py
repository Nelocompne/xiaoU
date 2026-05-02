import psutil
import datetime

def get_system_uptime():
    """
    获取系统开机时间和运行时间
    返回: (开机时间字符串, 运行时间字符串)
    """
    boot_time_timestamp = psutil.boot_time()
    boot_time = datetime.datetime.fromtimestamp(boot_time_timestamp)
    current_time = datetime.datetime.now()
    uptime = current_time - boot_time
    
    # 格式化开机时间
    boot_time_str = boot_time.strftime("%Y-%m-%d %H:%M:%S")
    
    # 格式化运行时间
    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    if days > 0:
        uptime_str = f"{days}天{hours}小时{minutes}分钟"
    else:
        uptime_str = f"{hours}小时{minutes}分钟"
    
    return boot_time_str, uptime_str

if __name__ == "__main__":
    boot_time, uptime = get_system_uptime()
    print(f"开机时间: {boot_time}")
    print(f"运行时间: {uptime}")