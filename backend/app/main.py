from fastapi import FastAPI

# Import Routers
from app.routers import users

app = FastAPI()

# Include Routers
app.include_router(users.router)

@app.get("/health")
def health():
    return {"status": "ok"}
