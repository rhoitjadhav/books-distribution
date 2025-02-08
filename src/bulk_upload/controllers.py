from fastapi import APIRouter, UploadFile, Response

from bulk_upload.services import BulkUploadService
from common.decorators import validate_file

router = APIRouter(prefix="/bulk-upload")


@router.post("")
@validate_file
async def process_bulk_upload(
    response: Response,
    file: UploadFile,
    table_name: str,
    batch_size: int = 1000,
    chunk_size: int = 1000,
):
    return await BulkUploadService(
        response, batch_size, chunk_size
    ).process_bulk_upload(file, table_name)
