from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from web.helpers import handle_place, handle_play, parse_data

app = FastAPI()

app.mount("/static", StaticFiles(directory="web/static"), name="static")
templates = Jinja2Templates(directory="web/templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/random", response_class=JSONResponse)
async def random(request: Request, state):
    ...


@app.post("/place", response_class=JSONResponse)
async def place(request: Request):
    data = await request.json()
    response_data = handle_place(*parse_data(data))
    if response_data is None:
        raise HTTPException(409, "Action not valid for given state")
    return JSONResponse(response_data)


@app.post("/play", response_class=JSONResponse)
async def play(request: Request):
    data = await request.json()
