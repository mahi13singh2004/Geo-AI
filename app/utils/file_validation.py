import os
import zipfile
from typing import Tuple
from app.core.config import settings


ALLOWED_EXTENSIONS = {".kml", ".zip"}
SHAPEFILE_REQUIRED_COMPONENTS = {".shp", ".shx", ".dbf"}


def validate_file_extension(filename: str) -> Tuple[bool, str]:
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False, "UNSUPPORTED_FILE_TYPE"
    return True, ext


def validate_file_size(file_size: int) -> Tuple[bool, str]:
    max_size = settings.MAX_FILE_SIZE_MB * 1024 * 1024
    if file_size > max_size:
        return False, "FILE_TOO_LARGE"
    return True, ""
