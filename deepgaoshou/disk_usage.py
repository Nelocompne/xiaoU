import psutil
import platform

def check_disk_usage(mount_point=None):
    """
    检查指定挂载点的磁盘使用情况
    返回: (总空间GB, 已用空间GB, 剩余空间GB, 使用百分比)
    """
    try:
        # 如果没有指定挂载点，根据操作系统选择默认值
        if mount_point is None:
            if platform.system() == "Windows":
                mount_point = "C:\\"
            else:
                mount_point = "/"
        
        # 在 Windows 上确保路径格式正确
        if platform.system() == "Windows":
            # 移除末尾的反斜杠（如果有多个）
            mount_point = mount_point.rstrip('\\')
            # 确保路径以单个反斜杠结尾
            if not mount_point.endswith('\\'):
                mount_point += '\\'
        
        disk_usage = psutil.disk_usage(mount_point)
        
        total_gb = round(disk_usage.total / (1024 ** 3), 2)
        used_gb = round(disk_usage.used / (1024 ** 3), 2)
        free_gb = round(disk_usage.free / (1024 ** 3), 2)
        percent = round(disk_usage.percent, 2)
        
        return total_gb, used_gb, free_gb, percent
    except Exception as e:
        print(f"检查磁盘使用情况时出错: {e}")
        print(f"尝试的挂载点: {mount_point}")
        return 0, 0, 0, 0

def get_available_drives():
    """
    获取系统中所有可用的驱动器（仅Windows）
    """
    if platform.system() != "Windows":
        return ["/"]
    
    import string
    from ctypes import windll
    
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(f"{letter}:\\")
        bitmask >>= 1
    
    return drives

if __name__ == "__main__":
    # 测试所有驱动器
    if platform.system() == "Windows":
        drives = get_available_drives()
        for drive in drives:
            total, used, free, percent = check_disk_usage(drive)
            print(f"驱动器 {drive}:")
            print(f"  总空间: {total}GB")
            print(f"  已用空间: {used}GB")
            print(f"  剩余空间: {free}GB")
            print(f"  使用率: {percent}%")
    else:
        total, used, free, percent = check_disk_usage()
        print(f"总空间: {total}GB")
        print(f"已用空间: {used}GB")
        print(f"剩余空间: {free}GB")
        print(f"使用率: {percent}%")