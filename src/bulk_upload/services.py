import csv

from fastapi import Response, UploadFile, HTTPException

from repositories.helpers.repository_helper import RepositoryHelper


class BulkUploadService:
    def __init__(self, response: Response, batch_size: int, chunk_size: int):
        self._response = response
        self._batch_size = batch_size
        self._chunk_size = chunk_size

    async def process_bulk_upload(self, file: UploadFile, table_name: str):
        contents = await file.read()
        file.file.seek(0)
        decoded_content = contents.decode("utf-8").splitlines()
        reader = csv.DictReader(decoded_content)

        if not reader.fieldnames:
            raise HTTPException(
                status_code=400, detail="CSV file is empty or invalid format"
            )

        values = [dict(row) for row in reader]
        RepositoryHelper().create(table_name, values)
        return {"message": f"Data successfully uploaded to {table_name}"}
