from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.gui import landing 
from src.api import health
from src.api import mask

app = FastAPI()

# mount static files as directory
app.mount("/static", StaticFiles(directory="src/static"), name="static")

# include routers
app.include_router(landing.router)
app.include_router(health.router, prefix="/api")
app.include_router(mask.router, prefix="/api")

# run the app if this file is executed
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)