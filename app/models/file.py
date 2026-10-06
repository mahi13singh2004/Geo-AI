from datetime import datetime
from typing import Optional


class FileModel:
    def __init__(
        self,
        id: str,
        filename: str,
        file_hash: str,
        file_type: str,
        file_size: int,
        crs: Optional[str],
        feature_count: int,
        status: str,
        storage_path: str,
        error_message: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id
        self.filename = filename
        self.file_hash = file_hash
        self.file_type = file_type
        self.file_size = file_size
        self.crs = crs
        self.feature_count = feature_count
        self.status = status
        self.storage_path = storage_path
        self.error_message = error_message
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
