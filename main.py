from fastapi import FastAPI
from backend.database.database import Base, engine
from backend.auth.routes import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth_router)

@app.get("/")
def home():
    return {"status": "Backend running"}