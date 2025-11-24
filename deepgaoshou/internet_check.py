import subprocess
import platform
import time

def check_internet_connection(hosts=None, timeout=5):
    """
    检查网络连接状态，支持多个备选host地址
    参数:
        hosts: 要检测的host列表，如果为None则使用默认列表
        timeout: 每次检测的超时时间（秒）
    返回: Boolean - 是否联网成功
    """
    if hosts is None:
        # 默认的备选host列表
        hosts = [
            "8.8.8.8",           # Google DNS
            "1.1.1.1",           # Cloudflare DNS
            "208.67.222.222",    # OpenDNS
            "223.5.5.5",         # 阿里云DNS
            "114.114.114.114"    # 114DNS
        ]
    
    # 根据操作系统选择ping参数
    param = "-n" if platform.system().lower() == "windows" else "-c"
    
    for host in hosts:
        try:
            # 执行ping命令
            result = subprocess.run(
                ["ping", param, "1", host],
                capture_output=True,
                timeout=timeout
            )
            
            # 如果ping成功，返回True
            if result.returncode == 0:
                return True
                
        except subprocess.TimeoutExpired:
            # 超时继续尝试下一个host
            continue
        except Exception:
            # 其他异常继续尝试下一个host
            continue
    
    # 所有host都失败，返回False
    return False

def check_internet_connection_with_details(hosts=None, timeout=5):
    """
    检查网络连接状态并返回详细信息
    参数:
        hosts: 要检测的host列表，如果为None则使用默认列表
        timeout: 每次检测的超时时间（秒）
    返回: (Boolean, str) - (是否联网成功, 详细信息)
    """
    if hosts is None:
        # 默认的备选host列表
        hosts = [
            "211.141.85.68",     # 移动DNS
            "211.141.90.68",     # 移动备选DNS
            "1.1.1.1",           # Cloudflare DNS
            "223.5.5.5",         # 阿里云DNS
            "114.114.114.114"    # 114DNS
        ]
    
    # 根据操作系统选择ping参数
    param = "-n" if platform.system().lower() == "windows" else "-c"
    
    failed_hosts = []
    
    for host in hosts:
        try:
            # 执行ping命令
            start_time = time.time()
            result = subprocess.run(
                ["ping", param, "1", host],
                capture_output=True,
                timeout=timeout
            )
            response_time = round((time.time() - start_time) * 1000, 2)
            
            # 如果ping成功，返回True和详细信息
            if result.returncode == 0:
                return True, f"成功连接到 {host} (响应时间: {response_time}ms)"
            else:
                failed_hosts.append(f"{host} (超时)")
                
        except subprocess.TimeoutExpired:
            failed_hosts.append(f"{host} (超时)")
        except Exception as e:
            failed_hosts.append(f"{host} (错误: {str(e)})")
    
    # 所有host都失败，返回False和错误信息
    error_msg = f"所有host连接失败: {', '.join(failed_hosts)}"
    return False, error_msg

if __name__ == "__main__":
    # 测试基本功能
    print("测试网络连接...")
    if check_internet_connection():
        print("网络连接正常")
    else:
        print("网络连接失败")
    
    # 测试详细功能
    print("\n测试详细网络连接信息...")
    status, details = check_internet_connection_with_details()
    print(f"状态: {'正常' if status else '失败'}")
    print(f"详情: {details}")
    
    # 测试自定义host列表
    print("\n测试自定义host列表...")
    custom_hosts = ["8.8.8.8", "1.1.1.1"]
    status, details = check_internet_connection_with_details(hosts=custom_hosts)
    print(f"状态: {'正常' if status else '失败'}")
    print(f"详情: {details}")