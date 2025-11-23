import json
import os
import time
from datetime import datetime
import psutil

def get_boot_time_simple():
    """使用psutil获取开机时间（推荐）"""
    try:
        boot_timestamp = psutil.boot_time()
        return datetime.fromtimestamp(boot_timestamp)
    except Exception as e:
        print(f"获取开机时间失败: {e}")
        return datetime.now()

def save_boot_time(boot_time):
    """保存开机时间到JSON文件"""
    # 创建子文件夹
    time_dir = "str"
    if not os.path.exists(time_dir):
        os.makedirs(time_dir)
    
    # 准备数据
    boot_data = {
        "boot_time": boot_time.isoformat(),
        "boot_timestamp": boot_time.timestamp(),
        "record_time": datetime.now().isoformat(),
        "record_timestamp": time.time()
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
    boot_time = get_boot_time_simple()
    
    # 显示结果
    print(f"系统开机时间: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 保存到文件
    if save_boot_time(boot_time):
        print("开机时间记录成功！")
    else:
        print("开机时间记录失败！")

if __name__ == "__main__":
    main()