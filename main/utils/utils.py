import os
import filetype
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS
from mutagen import File as MutagenFile
from pypdf import PdfReader
from docx import Document
import zipfile
import mimetypes


def get_file_metadata(file,url):
    content_type, _ = mimetypes.guess_type(file.name)
    metadata = {}
    
    #stats = os.stat(file.name)
    #kind = filetype.guess(file.name)
    #mime_type = kind.mime if kind else 'application/octet-stream'
    
    metadata["file_name"] = file.name
    metadata["file_size"] = file.size
    metadata["file_extension"] = file.name.split(".")[-1]
    #metadata["content_type"] = content_type or mime_type or "application/octet-stream"
    # metadata["created_at"] = datetime.fromtimestamp(stats.st_ctime).strftime("%Y-%m-%d %H:%M:%S")
   # metadata["updated_at"] = datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
    
    metadata["writable"] = True
    metadata["readable"] = True
    metadata["executable"] = False

    if 'image':
        try:
            with Image.open(url) as img:
                metadata.update({
                    'image_format': img.format,
                    'image_mode': img.mode,
                    'resolution': list(img.size),
                    'color_depth': img.bits if hasattr(img, 'bits') else None
                })
                exif_data = {}
                if hasattr(img, '_getexif') and img._getexif():
                    for tag_id, value in img._getexif().items():
                        tag = TAGS.get(tag_id, tag_id)
                        exif_data[tag] = str(value)
                metadata['exif_data'] = exif_data
        except Exception as e:
            metadata['error'] = str(e)

    elif 'audio' in mime_type or 'video' in mime_type:
        try:
            audio = MutagenFile(file)
            if audio is not None:
                if hasattr(audio.info, 'length'):
                    metadata['duration'] = round(audio.info.length, 2)
                if hasattr(audio.info, 'bitrate'):
                    metadata['bitrate'] = audio.info.bitrate
                if hasattr(audio.info, 'sample_rate'):
                    metadata['sample_rate'] = audio.info.sample_rate
                audio_tags = {}
                if hasattr(audio, 'tags') and audio.tags:
                    for key, value in audio.tags.items():
                        audio_tags[str(key)] = str(value)
                metadata['tags'] = audio_tags
        except Exception as e:
            metadata['error'] = str(e)

    elif 'pdf' in mime_type:
        try:
            with open(file, 'rb') as pdf_file:
                pdf = PdfReader(pdf_file)
                pdf_info = {}
                if pdf.metadata:
                    for key, value in pdf.metadata.items():
                        pdf_info[str(key)] = str(value)
                metadata.update({
                    'number_of_pages': len(pdf.pages),
                    'pdf_info': pdf_info,
                    'is_encrypted': pdf.is_encrypted
                })
        except Exception as e:
            metadata['error'] = str(e)

    elif mime_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        try:
            doc = Document(file)
            core_properties = doc.core_properties
            metadata.update({
                'author': core_properties.author,
                'created': str(core_properties.created) if core_properties.created else None,
                'last_modified_by': core_properties.last_modified_by,
                'modified': str(core_properties.modified) if core_properties.modified else None,
                'title': core_properties.title,
                'paragraph_count': len(doc.paragraphs)
            })
        except Exception as e:
            metadata['error'] = str(e)

    elif mime_type == 'application/zip':
        try:
            with zipfile.ZipFile(file, 'r') as zip_ref:
                metadata.update({
                    'file_count': len(zip_ref.filelist),
                    'compressed_size': sum(zinfo.compress_size for zinfo in zip_ref.filelist),
                    'uncompressed_size': sum(zinfo.file_size for zinfo in zip_ref.filelist),
                    'compression_types': list(set(zinfo.compress_type for zinfo in zip_ref.filelist))
                })
        except Exception as e:
            metadata['error'] = str(e)
    
    # if mime_type.startswith("image") or mime_type in [
    #     "application/pdf",
    #     "text/plain",
    # ]:
    #     metadata["writable"] = False
    #     metadata["executable"] = False
    # else:
    #     metadata["writable"] = False
    #     metadata["executable"] = False


    return metadata


# import mimetypes
# from datetime import datetime


# def get_file_metadata(file):
#     content_type, _ = mimetypes.guess_type(file.name)
#     metadata = {}
#     metadata["owner"] = "Unknown"
#     metadata["file_name"] = file.name
#     metadata["file_size"] = file.size
#     metadata["file_extension"] = file.name.split(".")[-1]
#     metadata["content_type"] = content_type or "application/octet-stream"
#     metadata["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     metadata["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#     # Default file permissions for in-memory files
#     metadata["writable"] = True
#     metadata["readable"] = True
#     metadata["executable"] = False

#     # Check the file type using the MIME type or extension

#     # Update permissions based on the file type
#     if content_type:
#         # If it's an image or other common types, make it read-only and non-executable
#         if content_type.startswith("image") or content_type in [
#             "application/pdf",
#             "text/plain",
#         ]:
#             metadata["writable"] = (
#                 False  # Image files or PDFs are generally not writable in-memory
#             )
#             metadata["executable"] = False
#         else:
#             metadata["writable"] = False  # If it's some other type, assume non-writable
#             metadata["executable"] = False  # In-memory files can't be executed
#     else:
#         # If MIME type couldn't be guessed, make writable based on context
#         metadata["writable"] = (
#             False  # Assume not writable if we can't determine MIME type
#         )
#         metadata["executable"] = False  # Assume not executable by default

#     return metadata
