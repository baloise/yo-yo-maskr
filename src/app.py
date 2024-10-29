from fastapi import FastAPI

from src.gui import landing
from src.api import health
from src.api import mask

app = FastAPI()

app.include_router(landing.router)
app.include_router(health.router, prefix="/api")
app.include_router(mask.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)