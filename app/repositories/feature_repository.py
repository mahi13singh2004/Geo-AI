import sqlite3
from typing import List, Optional, Tuple
from app.models.feature import FeatureModel
from app.core.config import settings
import json


class FeatureRepository:
    def __init__(self):
        self.db_path = settings.DATABASE_URL.replace("sqlite:///", "")
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS features (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_id TEXT NOT NULL,
                feature_index INTEGER NOT NULL,
                geometry_type TEXT NOT NULL,
                geometry TEXT NOT NULL,
                properties TEXT,
                source_crs TEXT,
                measurement_crs TEXT,
                measurement_type TEXT,
                measurement_value REAL,
                measurement_unit TEXT,
                measurement_status TEXT NOT NULL,
                FOREIGN KEY (file_id) REFERENCES files(id)
            )
        """
        )
        conn.commit()
        conn.close()

    def save_batch(self, features: List[FeatureModel]) -> None:
        if not features:
            return
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        for feature in features:
            cursor.execute(
                """
                INSERT INTO features VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    None,
                    feature.file_id,
                    feature.feature_index,
                    feature.geometry_type,
                    feature.geometry,
                    json.dumps(feature.properties) if feature.properties else None,
                    feature.source_crs,
                    feature.measurement_crs,
                    feature.measurement_type,
                    feature.measurement_value,
                    feature.measurement_unit,
                    feature.measurement_status,
                ),
            )
        conn.commit()
        conn.close()


    def get_by_file_id(
        self, file_id: str, limit: int, offset: int
    ) -> List[FeatureModel]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM features WHERE file_id = ? ORDER BY feature_index LIMIT ? OFFSET ?
        """,
            (file_id, limit, offset),
        )
        rows = cursor.fetchall()
        conn.close()

        features = []
        for row in rows:
            properties = json.loads(row[5]) if row[5] else None
            features.append(
                FeatureModel(
                    id=row[0],
                    file_id=row[1],
                    feature_index=row[2],
                    geometry_type=row[3],
                    geometry=row[4],
                    properties=properties,
                    source_crs=row[6],
                    measurement_crs=row[7],
                    measurement_type=row[8],
                    measurement_value=row[9],
                    measurement_unit=row[10],
                    measurement_status=row[11],
                )
            )
        return features

    def count_by_file_id(self, file_id: str) -> int:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM features WHERE file_id = ?", (file_id,))
        count = cursor.fetchone()[0]
        conn.close()
        return count
