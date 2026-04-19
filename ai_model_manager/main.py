from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.config.database import engine, Base
from app.config.settings import APP_NAME, APP_VERSION
from app.router.model_router import router
from app.model import model_entity
from app.router.chat_router import router as chat_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title=APP_NAME, version=APP_VERSION, lifespan=lifespan)
app.include_router(router)
app.include_router(chat_router)

@app.get("/")
def root():
    return {"message": f"欢迎使用 {APP_NAME}"}