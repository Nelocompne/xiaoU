import subprocess
import time
import requests
import platform

def check_internet_connection():
    """
    检测互联网连接
    返回: True如果有连接，False如果没有连接
    """
    try:
        # 尝试连接到一个可靠的网站
        response = requests.get("http://www.bilibili.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False
    except:
        return False

def execute_command():
    """
    检测到联网后要执行的命令
    """
    system = platform.system().lower()
    
    if system == "windows":
        # Windows 系统的命令示例
        commands = [
            ["echo", "网络已连接！执行命令..."],
            ["ipconfig"],
            # 可以添加更多命令，例如：
            # ["dir", "C:\\"],
            # ["ping", "google.com"]
        ]
    else:
        # Linux/Mac 系统的命令示例
        commands = [
            ["echo", "网络已连接！执行命令..."],
            ["ifconfig"],
            # 可以添加更多命令，例如：
            # ["ls", "-la"],
            # ["ping", "-c", "4", "google.com"]
        ]
    
    # 执行所有命令
    for cmd in commands:
        try:
            print(f"执行命令: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            print("输出:", result.stdout)
            if result.stderr:
                print("错误:", result.stderr)
            print("-" * 50)
        except subprocess.TimeoutExpired:
            print(f"命令超时: {' '.join(cmd)}")
        except Exception as e:
            print(f"执行命令时出错: {e}")

def main():
    """
    主函数 - 持续检测网络连接
    """
    print("开始检测网络连接...")
    print("程序将持续运行，直到检测到网络连接")
    print("按 Ctrl+C 可以退出程序")
    
    already_executed = False
    
    try:
        while True:
            if check_internet_connection():
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 检测到互联网连接！")
                
                if not already_executed:
                    execute_command()
                    already_executed = True
                    print("命令执行完成，程序继续运行...")
                else:
                    print("命令已经执行过，跳过...")
            else:
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 无互联网连接，继续检测...")
                already_executed = False  # 重置状态，以便网络断开重连后再次执行
            
            # 等待5秒后再次检测
            time.sleep(5)
                
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"程序发生错误: {e}")

if __name__ == "__main__":
    main()