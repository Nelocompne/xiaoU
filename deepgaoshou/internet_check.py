import subprocess
import platform

def check_internet_connection(host="8.8.8.8"):
    """
    检查网络连接状态
    返回: Boolean - 是否联网成功
    """
    try:
        # 根据操作系统选择ping参数
        param = "-n" if platform.system().lower() == "windows" else "-c"
        
        # 执行ping命令
        result = subprocess.run(
            ["ping", param, "1", host],
            capture_output=True,
            timeout=5
        )
        
        return result.returncode == 0
    except:
        return False

if __name__ == "__main__":
    if check_internet_connection():
        print("网络连接正常")
    else:
        print("网络连接失败")