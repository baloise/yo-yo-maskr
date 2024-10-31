from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.gui import gui_landing, gui_mask, gui_demaks
from src.api import health
from src.api import mask
from src.api import demask

app = FastAPI()

# mount static files as directory
app.mount("/static", StaticFiles(directory="src/static"), name="static")

# include routers
## GUI
app.include_router(gui_landing.router)
app.include_router(gui_mask.router)
app.include_router(gui_demaks.router)

## API
app.include_router(health.router, prefix="/api")
app.include_router(mask.router, prefix="/api")
app.include_router(demask.router, prefix="/api")


# run the app if this file is executed
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)