import os,stat,platform
from datetime import datetime


def get_file_metadata(file, content_type):
 
        file_path = file.temporary_file_path() if hasattr(file, 'temporary_file_path') else None
        
        metadata = {
            "file_name": file.name,
            "file_size": file.size,
            "content_type": content_type or "application/octet-stream",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "owner": os.getlogin() if platform.system() == "Windows" else "Unknown",
            "file_extension": file.name.split('.')[-1],
            "writable":False,
            "executable":False,
            "readable":False
        }

        if file_path and os.path.exists(file_path):
            stats = os.stat(file_path)
            metadata.update({
                "writable": bool(stats.st_mode & stat.S_IWUSR) or os.access(file_path, os.W_OK),
                "readable": bool(stats.st_mode & stat.S_IRUSR) or os.access(file_path, os.R_OK),
                "executable": bool(stats.st_mode & stat.S_IXUSR) or os.access(file_path, os.X_OK),
                "owner": os.getlogin(),
            })

        if content_type in ["application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", 
                        "application/pdf", "text/plain"]:
            metadata.update({"readable": True, "writable": True, "executable": False})

        
        return metadata