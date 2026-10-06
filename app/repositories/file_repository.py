import sqlite3
from typing import Optional
from app.models.file import FileModel
from app.core.config import settings
import json


class FileRepository:
    def __init__(self):
        self.db_path = settings.DATABASE_URL.replace("sqlite:///", "")
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS files (
                id TEXT PRIMARY KEY,
                filename TEXT NOT NULL,
                file_hash TEXT NOT NULL UNIQUE,
                file_type TEXT NOT NULL,
                file_size INTEGER NOT NULL,
                crs TEXT,
                feature_count INTEGER DEFAULT 0,
                status TEXT NOT NULL,
                storage_path TEXT NOT NULL,
                error_message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        conn.commit()
        conn.close()

    def save(self, file_model: FileModel) -> None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO files VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                file_model.id,
                file_model.filename,
                file_model.file_hash,
                file_model.file_type,
                file_model.file_size,
                file_model.crs,
                file_model.feature_count,
                file_model.status,
                file_model.storage_path,
                file_model.error_message,
                file_model.created_at,
                file_model.updated_at,
            ),
        )
        conn.commit()
        conn.close()


    def get_by_id(self, file_id: str) -> Optional[FileModel]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM files WHERE id = ?", (file_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        return FileModel(
            id=row[0],
            filename=row[1],
            file_hash=row[2],
            file_type=row[3],
            file_size=row[4],
            crs=row[5],
            feature_count=row[6],
            status=row[7],
            storage_path=row[8],
            error_message=row[9],
        )

    def update_status(
        self, file_id: str, status: str, feature_count: int, crs: Optional[str], error_message: Optional[str] = None
    ):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE files 
            SET status = ?, feature_count = ?, crs = ?, error_message = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """,
            (status, feature_count, crs, error_message, file_id),
        )
        conn.commit()
        conn.close()

    def get_by_hash(self, file_hash: str) -> Optional[FileModel]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM files WHERE file_hash = ?", (file_hash,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        return FileModel(
            id=row[0],
            filename=row[1],
            file_hash=row[2],
            file_type=row[3],
            file_size=row[4],
            crs=row[5],
            feature_count=row[6],
            status=row[7],
            storage_path=row[8],
            error_message=row[9],
        )
