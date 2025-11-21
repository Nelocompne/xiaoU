import psutil
import json
import os
import time
from datetime import datetime

def monitor_disk_simple(mount_point=None, check_interval=5):
    """
    简化版磁盘监控
    
    Args:
        mount_point: 监控的挂载点
        check_interval: 检查间隔
    """
    # 设置默认挂载点
    if mount_point is None:
        mount_point = 'D:\\' if os.name == 'nt' else '/'
    
    # 创建输出目录
    output_dir = "str"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print(f"开始监控磁盘: {mount_point}")
    print(f"数据保存到: {output_dir}/disk.json")
    print("按 Ctrl+C 停止监控\n")
    
    try:
        while True:
            # 获取磁盘使用情况
            disk_usage = psutil.disk_usage(mount_point)
            used_percent = (disk_usage.used / disk_usage.total) * 100
            free_percent = (disk_usage.free / disk_usage.total) * 100
            
            # 准备数据
            disk_data = {
                "mount_point": mount_point,
                "used_percent": round(used_percent, 2),
                "free_percent": round(free_percent, 2),
                "total_gb": round(disk_usage.total / (1024**3), 2),
                "used_gb": round(disk_usage.used / (1024**3), 2),
                "free_gb": round(disk_usage.free / (1024**3), 2),
                "timestamp": datetime.now().isoformat()
            }
            
            # 保存到JSON文件
            file_path = os.path.join(output_dir, "disk.json")
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(disk_data, f, ensure_ascii=False, indent=4)
            
            # 打印状态
            print(f"[{datetime.now().strftime('%H:%M:%S')}] "
                  f"使用率: {used_percent:.1f}% | 剩余: {free_percent:.1f}%")
            
            time.sleep(check_interval)
            
    except KeyboardInterrupt:
        print("\n监控已停止")

if __name__ == "__main__":
    # 直接监控系统盘，每5秒检查一次
    monitor_disk_simple()