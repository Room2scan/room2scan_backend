from sqlalchemy.orm import Session
from app.db.models import Image, Furniture, Placement

def get_images(db: Session):
    return db.query(Image).all()

def get_image_by_id(db: Session, image_id: int):
    return db.query(Image).filter(Image.id==image_id).first()

# 전체 조회
def get_furniture(db: Session):
    return db.query(Furniture).all()

# 단일 조회
def get_furniture_by_id(db: Session, furniture_id: int):
    return db.query(Furniture).filter(Furniture.id == furniture_id).first()

# 생성
def create_furniture(db: Session, name: str, model_url: str, thumbnail_url: str):
    item = Furniture(
        name=name,
        model_url=model_url,
        thumbnail_url=thumbnail_url
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

# 삭제
def delete_furniture(db: Session, furniture_id: int):
    item = get_furniture_by_id(db, furniture_id)
    if item:
        db.delete(item)
        db.commit()
    return item

def create_placement(db, image_id, furniture_id, x, y, z, rotation):
    item = Placement(
        image_id=image_id,
        furniture_id=furniture_id,
        x=x,
        y=y,
        z=z,
        rotation=rotation
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def get_placements_by_image(db, image_id):
    return db.query(Placement).filter(Placement.image_id == image_id).all()

def update_placement(db, placement_id, x, y, z, rotation):
    item = db.query(Placement).filter(Placement.id == placement_id).first()

    if not item:
        return None

    item.x = x
    item.y = y
    item.z = z
    item.rotation = rotation

    db.commit()
    db.refresh(item)

    return item

def delete_placement(db, placement_id: int):
    item = db.query(Placement).filter(Placement.id == placement_id).first()

    if not item:
        return None

    db.delete(item)
    db.commit()

    return item