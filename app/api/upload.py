from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
import uuid
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.crud import get_images, get_image_by_id
from app.core.s3 import upload_to_s3, delete_from_s3
from app.db.models import Image

router = APIRouter(tags=["Image"])

# 업로드 
@router.post("/upload")
async def upload(file: UploadFile = File(...), db: Session = Depends(get_db)):
    filename = f"{uuid.uuid4()}.jpg"

    # S3 업로드
    url = upload_to_s3(file.file, filename)

    # DB 저장
    new_image = Image(file_url=url)

    db.add(new_image)
    db.commit()
    db.refresh(new_image)

    return {
        "image_id": new_image.id,
        "file_url": url
    }


# 이미지 리스트 조회
@router.get("/images")
def read_images(db: Session = Depends(get_db)):
    images = get_images(db)

    return [
        {
            "id": img.id,
            "file_url": img.file_url
        }
        for img in images
    ]

@router.get("/images/{image_id}")
def read_image(image_id: int, db: Session = Depends(get_db)):
    image = get_image_by_id(db, image_id)

    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    return {
        "id": image.id,
        "file_url": image.file_url,
        "mesh_url": image.mesh_url
    }

@router.post("/mesh-upload/{image_id}", tags=["Mesh"])
async def upload_mesh(
    image_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 파일 이름 생성
    filename = f"{uuid.uuid4()}.obj"  # 필요하면 .glb로 바꿔도 됨

    # S3 업로드
    url = upload_to_s3(file.file, filename)

    # DB 조회
    image = db.query(Image).filter(Image.id == image_id).first()

    if not image:
        return {"error": "Image not found"}

    # mesh_url 저장
    image.mesh_url = url
    db.commit()

    return {
        "message": "mesh uploaded",
        "mesh_url": url
    }

# 삭제
@router.delete("/images/{image_id}")
def delete_image(image_id: int, db: Session = Depends(get_db)):
    image = db.query(Image).filter(Image.id == image_id).first()

    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    # S3 삭제
    if image.file_url:
        delete_from_s3(image.file_url)

    if image.mesh_url:
        delete_from_s3(image.mesh_url)

    # DB 삭제
    db.delete(image)
    db.commit()

    return {"message": "image deleted"}