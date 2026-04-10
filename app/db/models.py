from sqlalchemy import Column, Integer, String
from app.db.database import Base

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    file_url = Column(String)
    mesh_url=Column(String, nullable=True)

class Furniture(Base):
    __tablename__ = "furniture"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    model_url = Column(String)       # 3D 모델 (.glb, .obj)
    thumbnail_url = Column(String)   # 썸네일 이미지

class Placement(Base):
    __tablename__ = "placements"

    id = Column(Integer, primary_key=True, index=True)

    image_id = Column(Integer)        # 어떤 방인지
    furniture_id = Column(Integer)    # 어떤 가구인지

    x = Column(String)  # 위치
    y = Column(String)
    z = Column(String)

    rotation = Column(String)  # 회전값