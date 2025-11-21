import json
import os
import platform
import subprocess
import time
from datetime import datetime

def get_boot_time():
    """获取系统开机时间"""
    system = platform.system().lower()
    
    try:
        if system == "windows":
            # Windows系统
            cmd = 'systeminfo | find "系统启动时间"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='gbk')
            if result.returncode == 0:
                boot_time_str = result.stdout.strip()
                # 解析时间字符串，格式如：系统启动时间:            2024/1/1, 12:00:00
                parts = boot_time_str.split(':', 1)
                if len(parts) > 1:
                    time_str = parts[1].strip()
                    # 尝试解析不同格式的时间
                    for fmt in ['%Y/%m/%d, %H:%M:%S', '%Y-%m-%d %H:%M:%S']:
                        try:
                            boot_time = datetime.strptime(time_str, fmt)
                            return boot_time
                        except ValueError:
                            continue
            
        elif system == "linux":
            # Linux系统
            with open('/proc/uptime', 'r') as f:
                uptime_seconds = float(f.readline().split()[0])
            boot_time = datetime.now().timestamp() - uptime_seconds
            return datetime.fromtimestamp(boot_time)
            
        elif system == "darwin":
            # macOS系统
            cmd = 'sysctl -n kern.boottime'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                # 输出格式：{ sec = 1700000000, usec = 0 } 2024-01-01 12:00:00
                boot_timestamp = int(result.stdout.strip().split(' ')[2].rstrip(','))
                return datetime.fromtimestamp(boot_timestamp)
    
    except Exception as e:
        print(f"获取开机时间时出错: {e}")
    
    # 如果上述方法都失败，使用备用方法
    try:
        # 使用psutil库（如果安装的话）
        import psutil
        boot_timestamp = psutil.boot_time()
        return datetime.fromtimestamp(boot_timestamp)
    except ImportError:
        print("psutil未安装，使用备用方法")
        # 最终备用方法：使用当前时间减去系统运行时间
        if system == "windows":
            # Windows备用方法
            cmd = 'wmic os get lastbootuptime'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if len(lines) > 1:
                    time_str = lines[1].strip()
                    # 格式：20240101120000.000000+480
                    try:
                        return datetime.strptime(time_str[:14], '%Y%m%d%H%M%S')
                    except ValueError:
                        pass
    
    # 如果所有方法都失败，返回当前时间（作为默认值）
    print("无法获取准确的开机时间，使用当前时间作为默认值")
    return datetime.now()

def save_boot_time(boot_time):
    """保存开机时间到JSON文件"""
    # 创建子文件夹
    time_dir = "time"
    if not os.path.exists(time_dir):
        os.makedirs(time_dir)
    
    # 准备数据
    boot_data = {
        "boot_time": boot_time.isoformat(),
        "boot_timestamp": boot_time.timestamp(),
        "record_time": datetime.now().isoformat(),
        "record_timestamp": time.time(),
        "system": platform.system(),
        "version": platform.version()
    }
    
    # 保存到文件
    file_path = os.path.join(time_dir, "date.json")
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(boot_data, f, ensure_ascii=False, indent=4)
        print(f"开机时间已保存到: {file_path}")
        return True
    except Exception as e:
        print(f"保存文件时出错: {e}")
        return False

def main():
    """主函数"""
    print("正在获取系统开机时间...")
    
    # 获取开机时间
    boot_time = get_boot_time()
    
    # 显示结果
    print(f"系统开机时间: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"已运行时间: {datetime.now() - boot_time}")
    
    # 保存到文件
    if save_boot_time(boot_time):
        print("开机时间记录成功！")
    else:
        print("开机时间记录失败！")

if __name__ == "__main__":
    main()