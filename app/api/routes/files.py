from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas.file import FileUploadResponse, FileInfoResponse
from app.services.file_service import FileService
import logging

logger = logging.getLogger(__name__)
router = APIRouter()
file_service = FileService()


@router.post("/files/", response_model=FileUploadResponse)
async def upload_file(file: UploadFile = File(...)):
    try:
        result = await file_service.upload_and_process(file)
        return FileUploadResponse(
            id=result.id, filename=result.filename, status=result.status
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Upload failed: {str(e)}")
        raise HTTPException(status_code=500, detail="FILE_PROCESSING_FAILED")


@router.get("/files/{file_id}/", response_model=FileInfoResponse)
async def get_file_info(file_id: str):
    try:
        result = file_service.get_file_info(file_id)
        if not result:
            raise HTTPException(status_code=404, detail="FILE_NOT_FOUND")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get file info failed: {str(e)}")
        raise HTTPException(status_code=500, detail="INTERNAL_ERROR")
