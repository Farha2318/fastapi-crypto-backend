from fastapi import FastAPI
from fiat.routes import router as fiat_router

app = FastAPI(title="FastAPI Crypto Backend")

app.include_router(fiat_router)

@app.get("/")
def root():
    return {"message": "FastAPI Crypto Backend running"}
