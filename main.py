import os
from fastapi import FastAPI

app = FastAPI()
VERSION = os.getenv("APP_VERSION", "dev")


@app.get("/")
def root():
    return {"message": "hello from demo-app", "version": VERSION}


@app.get("/health")
def health():
    return {"status": "ok"}
