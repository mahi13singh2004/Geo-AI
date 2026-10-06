from fastapi import APIRouter, HTTPException, Query
from app.schemas.measurement import MeasurementsResponse
from app.services.file_service import FileService
import logging

logger = logging.getLogger(__name__)
router = APIRouter()
file_service = FileService()


@router.get("/files/{file_id}/measurements/", response_model=MeasurementsResponse)
async def get_measurements(
    file_id: str, page: int = Query(1, ge=1), limit: int = Query(100, ge=1, le=1000)
):
    try:
        result = file_service.get_measurements(file_id, page, limit)
        if not result:
            raise HTTPException(status_code=404, detail="FILE_NOT_FOUND")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get measurements failed: {str(e)}")
        raise HTTPException(status_code=500, detail="INTERNAL_ERROR")
