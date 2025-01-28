import mimetypes
from datetime import datetime


def get_file_metadata(file):
    content_type, _ = mimetypes.guess_type(file.name)
    metadata = {}
    metadata["owner"] = "Unknown"
    metadata["file_name"] = file.name
    metadata["file_size"] = file.size
    metadata["file_extension"] = file.name.split(".")[-1]
    metadata["content_type"] = content_type or "application/octet-stream"
    metadata["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    metadata["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Default file permissions for in-memory files
    metadata["writable"] = True
    metadata["readable"] = True
    metadata["executable"] = False

    # Check the file type using the MIME type or extension

    # Update permissions based on the file type
    if content_type:
        # If it's an image or other common types, make it read-only and non-executable
        if content_type.startswith("image") or content_type in [
            "application/pdf",
            "text/plain",
        ]:
            metadata["writable"] = (
                False  # Image files or PDFs are generally not writable in-memory
            )
            metadata["executable"] = False
        else:
            metadata["writable"] = False  # If it's some other type, assume non-writable
            metadata["executable"] = False  # In-memory files can't be executed
    else:
        # If MIME type couldn't be guessed, make writable based on context
        metadata["writable"] = (
            False  # Assume not writable if we can't determine MIME type
        )
        metadata["executable"] = False  # Assume not executable by default

    return metadata
