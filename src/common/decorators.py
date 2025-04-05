import functools

from fastapi import HTTPException


def validate_file(func):
    """Decorator to validate file type and size"""
    ALLOWED_TYPES = {"text/csv"}
    MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB
    CHUNK_SIZE = 1024 * 1024  # 1MB chunks

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        file = kwargs.get("file")
        if not file:
            raise HTTPException(status_code=422, detail="No file uploaded")
        if file.content_type not in ALLOWED_TYPES:
            raise HTTPException(status_code=400, detail="File type not allowed")

        total_size = 0
        while chunk := await file.read(CHUNK_SIZE):  # Read in chunks
            total_size += len(chunk)
            if total_size > MAX_FILE_SIZE:
                raise HTTPException(status_code=400, detail="File size exceeds limit")

        # Reset file pointer after validation
        file.file.seek(0)
        kwargs["file"] = file
        return await func(*args, **kwargs)

    return wrapper
