from fastapi import APIRouter, UploadFile
import shutil

router = APIRouter(
    prefix="/files",
    tags=["Вложения"])


@router.post("/beta_image")
async def add_atach_ticket(name: int, file: UploadFile):
    with open(f"app/static/files/{name}.webp", "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)