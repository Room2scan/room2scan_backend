from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.crud import create_placement, get_placements_by_image, update_placement,delete_placement

router = APIRouter(tags=["Placement"])


# 가구 배치 저장
@router.post("/")
def save_placement(
    image_id: int,
    furniture_id: int,
    x: str,
    y: str,
    z: str,
    rotation: str,
    db: Session = Depends(get_db)
):
    item = create_placement(
        db, image_id, furniture_id, x, y, z, rotation
    )

    return {
        "id": item.id,
        "message": "placement saved"
    }


# 특정 이미지의 배치 조회
@router.get("/{image_id}")
def read_placements(image_id: int, db: Session = Depends(get_db)):
    items = get_placements_by_image(db, image_id)

    return [
        {
            "id": i.id,
            "furniture_id": i.furniture_id,
            "x": i.x,
            "y": i.y,
            "z": i.z,
            "rotation": i.rotation
        }
        for i in items
    ]

@router.put("/{placement_id}")
def update_placement_api(
    placement_id: int,
    x: str,
    y: str,
    z: str,
    rotation: str,
    db: Session = Depends(get_db)
):
    updated = update_placement(db, placement_id, x, y, z, rotation)

    if not updated:
        raise HTTPException(status_code=404, detail="Placement not found")

    return {
        "message": "placement updated",
        "id": updated.id,
        "x": updated.x,
        "y": updated.y,
        "z": updated.z,
        "rotation": updated.rotation
    }

@router.delete("/{placement_id}")
def delete_placement_api(
    placement_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_placement(db, placement_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Placement not found")

    return {
        "message": "placement deleted",
        "id": placement_id
    }