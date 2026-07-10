from fastapi import FastAPI

# Import Routers
from app.routers import users
from app.routers import auth

app = FastAPI()

# Include Routers
app.include_router(users.router)
app.include_router(auth.router)

@app.get("/health")
def health():
    return {"status": "ok"}
