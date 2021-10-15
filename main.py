from fastapi import FastAPI, Request
import uvicorn
from app import routers

from app.database import open_database_connection_pool, close_database_connection_pool
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.on_event('startup')
def startup_event():
    open_database_connection_pool()


@app.on_event('shutdown')
def shutdown_event():
    close_database_connection_pool()


app.include_router(router=routers.account_router)

templates = Jinja2Templates(directory="templates")

from ImageClassification.AI_pipeline import get_image

@app.get("/test/image", response_class=HTMLResponse)
async def read_image(request: Request):
    _, image_path = get_image()
    return templates.TemplateResponse("test.html", {"request": request, "img_path": image_path})


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)







