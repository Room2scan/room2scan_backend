# app/api/furniture.py

from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

from app.db.database import get_db
from app.db.crud import (
    get_furniture,
    get_furniture_by_id,
    create_furniture,
    delete_furniture
)
from app.core.s3 import upload_to_s3

router = APIRouter(tags=["Furniture"])

# 1. 전체 조회
@router.get("/furniture")
def read_furniture(db: Session = Depends(get_db)):
    items = get_furniture(db)
    return [
        {
            "id": item.id,
            "name": item.name,
            "model_url": item.model_url,
            "thumbnail_url": item.thumbnail_url
        }
        for item in items
    ]


# 2. 상세 조회
@router.get("/furniture/{furniture_id}")
def read_furniture_detail(furniture_id: int, db: Session = Depends(get_db)):
    item = get_furniture_by_id(db, furniture_id)

    if not item:
        raise HTTPException(status_code=404, detail="Furniture not found")

    return {
        "id": item.id,
        "name": item.name,
        "model_url": item.model_url,
        "thumbnail_url": item.thumbnail_url
    }


# 3. 가구 추가 (파일 업로드 포함)
@router.post("/furniture")
async def upload_furniture(
    name: str = Form(...),
    model_file: UploadFile = File(...),
    thumbnail_file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    model_filename = f"{uuid.uuid4()}.glb"
    thumbnail_filename = f"{uuid.uuid4()}.png"

    # S3 업로드
    model_url = upload_to_s3(model_file.file, model_filename)
    thumbnail_url = upload_to_s3(thumbnail_file.file, thumbnail_filename)

    # DB 저장
    item = create_furniture(db, name, model_url, thumbnail_url)

    return {
        "id": item.id,
        "name": item.name,
        "model_url": model_url,
        "thumbnail_url": thumbnail_url
    }


# 4. 삭제
@router.delete("/furniture/{furniture_id}")
def remove_furniture(furniture_id: int, db: Session = Depends(get_db)):
    item = delete_furniture(db, furniture_id)

    if not item:
        raise HTTPException(status_code=404, detail="Furniture not found")

    return {"message": "furniture deleted"}