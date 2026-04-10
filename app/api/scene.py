from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.crud import (
    get_image_by_id,
    get_placements_by_image,
    get_furniture
)

router = APIRouter(tags=["Scene"])

@router.get("/{image_id}")
def get_scene(image_id: int, db: Session = Depends(get_db)):

    # 1. 이미지 조회
    image = get_image_by_id(db, image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    # 2. placement 조회
    placements = get_placements_by_image(db, image_id)

    # 3. furniture 조회
    furnitures = get_furniture(db)

    return {
        "image": {
            "id": image.id,
            "file_url": image.file_url,
            "mesh_url": image.mesh_url
        },
        "placements": [
            {
                "id": p.id,
                "furniture_id": p.furniture_id,
                "x": p.x,
                "y": p.y,
                "z": p.z,
                "rotation": p.rotation
            }
            for p in placements
        ],
        "furnitures": [
            {
                "id": f.id,
                "name": f.name,
                "model_url": f.model_url,
                "thumbnail_url": f.thumbnail_url
            }
            for f in furnitures
        ]
    }