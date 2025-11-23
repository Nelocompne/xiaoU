import psutil

def check_disk_usage(mount_point="/"):
    """
    检查指定挂载点的磁盘使用情况
    返回: (总空间GB, 已用空间GB, 剩余空间GB, 使用百分比)
    """
    try:
        disk_usage = psutil.disk_usage(mount_point)
        
        total_gb = round(disk_usage.total / (1024 ** 3), 2)
        used_gb = round(disk_usage.used / (1024 ** 3), 2)
        free_gb = round(disk_usage.free / (1024 ** 3), 2)
        percent = disk_usage.percent
        
        return total_gb, used_gb, free_gb, percent
    except Exception as e:
        print(f"检查磁盘使用情况时出错: {e}")
        return 0, 0, 0, 0

if __name__ == "__main__":
    total, used, free, percent = check_disk_usage()
    print(f"总空间: {total}GB")
    print(f"已用空间: {used}GB")
    print(f"剩余空间: {free}GB")
    print(f"使用率: {percent}%")