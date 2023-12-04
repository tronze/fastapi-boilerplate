from fastapi import FastAPI

from database import Base, engine


app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/health-check")
async def health_check():
    return
