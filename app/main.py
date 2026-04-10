from fastapi import FastAPI
from app.api import upload, furniture, placement, scene
from app.db.database import engine, Base
from app.db import models

# FastAPI 앱 생성
app = FastAPI()

# 라우터 등록
app.include_router(upload.router, prefix="/images")
app.include_router(furniture.router, prefix="/furniture")
app.include_router(placement.router, prefix="/placement")
app.include_router(scene.router, prefix="/scene")

# 테이블 생성
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "서버 잘 돌아간다"}