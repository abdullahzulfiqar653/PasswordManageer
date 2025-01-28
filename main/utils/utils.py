import os,stat,platform
from datetime import datetime 

if platform.system() != "Windows":
    import pwd

def get_file_metadata(file, content_type):
    file_path = file.temporary_file_path() if hasattr(file, 'temporary_file_path') else None
    metadata = {}
    metadata["file_name"] = file.name
    metadata["file_size"] = file.size
    metadata["content_type"] = content_type or "application/octet-stream"
    metadata["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    metadata["owner"] = os.getlogin() if platform.system() == "Windows" else "Unknown"
    metadata["file_extension"] = file.name.split('.')[-1]
    
    if platform.system() == "Windows":
        metadata["owner"] = os.getlogin()
    else:
        try:
            metadata["owner"] = pwd.getpwuid(os.stat(file_path).st_uid).pw_name
        except KeyError:
            metadata["owner"] = "Unknown"

    if file_path and os.path.exists(file_path):
        stats = os.stat(file_path)
        metadata["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        metadata["writable"] = bool(stats.st_mode & stat.S_IWUSR) or os.access(file_path, os.W_OK)
        metadata["readable"] = bool(stats.st_mode & stat.S_IRUSR) or os.access(file_path, os.R_OK)
        metadata["executable"] = bool(stats.st_mode & stat.S_IXUSR) or os.access(file_path, os.X_OK)
       
    return metadata
