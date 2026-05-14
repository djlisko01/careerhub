from fastapi import FastAPI

from backend.routers.v1 import auth

app = FastAPI()

# Add Routers Here
app.include_router(auth.router)


@app.get("/health")
def read_health():
    return {"status": "ok"}
