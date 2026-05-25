
def filter_file(commit, metadata):
    # 保留全功能整合包1.5的exe
    keep_path = "04-正式发行版/全功能整合包1.5/游戏修改器控制台_v1.5.exe"
    
    # 检查文件是否是我们要保留的
    if metadata.filename == keep_path:
        return True  # 保留
    # 删除所有其他 exe 文件
    elif metadata.filename.endswith(".exe"):
        return False  # 删除
    # 保留其他所有文件
    else:
        return True
