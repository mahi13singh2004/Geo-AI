import os
import uuid
import shutil
from fastapi import UploadFile
from app.models.file import FileModel
from app.repositories.file_repository import FileRepository
from app.repositories.feature_repository import FeatureRepository
from app.services.processing_service import ProcessingService
from app.utils.hashing import calculate_file_hash
from app.utils.file_validation import validate_file_extension, validate_file_size
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class FileService:
    def __init__(self):
        self.file_repo = FileRepository()
        self.feature_repo = FeatureRepository()
        self.processing_service = ProcessingService()

    async def upload_and_process(self, file: UploadFile) -> FileModel:
        is_valid, result = validate_file_extension(file.filename)
        if not is_valid:
            raise ValueError(result)

        file_extension = result
        temp_path = os.path.join(settings.UPLOAD_DIR, f"temp_{uuid.uuid4()}{file_extension}")

        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_size = os.path.getsize(temp_path)
        is_valid, error = validate_file_size(file_size)
        if not is_valid:
            os.remove(temp_path)
            raise ValueError(error)

        file_hash = calculate_file_hash(temp_path)
        file_id = str(uuid.uuid4())
        storage_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}{file_extension}")
        shutil.move(temp_path, storage_path)

        file_model = FileModel(
            id=file_id,
            filename=file.filename,
            file_hash=file_hash,
            file_type=file_extension,
            file_size=file_size,
            crs=None,
            feature_count=0,
            status="PROCESSING",
            storage_path=storage_path,
        )
        self.file_repo.save(file_model)

        try:
            features = self.processing_service.process_file(
                storage_path, file_id, file_extension
            )
            self.feature_repo.save_batch(features)

            file_model.status = "COMPLETED"
            file_model.feature_count = len(features)
            if features:
                file_model.crs = features[0].source_crs
            self.file_repo.update_status(file_id, "COMPLETED", len(features), file_model.crs)

            logger.info(f"file_processing_completed file_id={file_id}")
        except Exception as e:
            logger.error(f"File processing failed: {str(e)}")
            file_model.status = "FAILED"
            file_model.error_message = str(e)
            self.file_repo.update_status(file_id, "FAILED", 0, None, str(e))

        return file_model

    def get_file_info(self, file_id: str):
        return self.file_repo.get_by_id(file_id)

    def get_measurements(self, file_id: str, page: int, limit: int):
        file_info = self.file_repo.get_by_id(file_id)
        if not file_info:
            return None

        offset = (page - 1) * limit
        features = self.feature_repo.get_by_file_id(file_id, limit, offset)
        total = self.feature_repo.count_by_file_id(file_id)

        results = []
        for feature in features:
            measurement_detail = None
            if feature.measurement_value is not None:
                measurement_detail = {
                    "type": feature.measurement_type,
                    "value": feature.measurement_value,
                    "unit": feature.measurement_unit,
                }

            results.append({
                "feature_id": feature.feature_index,
                "geometry_type": feature.geometry_type,
                "measurement": measurement_detail,
                "measurement_status": feature.measurement_status,
            })

        return {
            "file_id": file_id,
            "page": page,
            "limit": limit,
            "total": total,
            "results": results,
        }
