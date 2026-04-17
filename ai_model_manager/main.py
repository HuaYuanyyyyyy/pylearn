from fastapi import FastAPI
from app.config.settings import APP_NAME, APP_VERSION
from app.router.model_router import router

app = FastAPI(title=APP_NAME, version=APP_VERSION)
app.include_router(router)

@app.get("/")
def root():
    return {"message": f"欢迎使用 {APP_NAME}"}