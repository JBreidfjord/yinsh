from urllib import response

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from web.helpers import (
    get_outcome,
    handle_bot,
    handle_bot_row,
    handle_dsts,
    handle_place,
    handle_play,
    handle_ring,
    handle_row,
    parse_data,
    parse_play_data,
)

app = FastAPI()

app.mount("/static", StaticFiles(directory="web/static"), name="static")
templates = Jinja2Templates(directory="web/templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/bot", response_class=JSONResponse)
async def bot(request: Request):
    data = await request.json()
    _, game = parse_data(data)
    response_data = handle_bot(game)
    return JSONResponse(response_data)


@app.post("/bot-row", response_class=JSONResponse)
async def bot_row(request: Request):
    data = await request.json()
    _, game = parse_data(data)
    response_data = handle_bot_row(game)
    return JSONResponse(response_data)


@app.post("/place", response_class=JSONResponse)
async def place(request: Request):
    data = await request.json()
    response_data = handle_place(*parse_data(data))
    if response_data is None:
        raise HTTPException(409, "Action not valid for given state")
    return JSONResponse(response_data)


@app.post("/play-src", response_class=JSONResponse)
async def play_src(request: Request):
    data = await request.json()
    response_data = handle_dsts(*parse_data(data))
    if response_data is None:
        raise HTTPException(409, "Action not valid for given state")
    return JSONResponse(response_data)


@app.post("/play-dst", response_class=JSONResponse)
async def play_dst(request: Request):
    data = await request.json()
    response_data = handle_play(*parse_play_data(data))
    if response_data is None:
        raise HTTPException(409, "Action not valid for given state")
    return JSONResponse(response_data)


@app.post("/row", response_class=JSONResponse)
async def row(request: Request):
    data = await request.json()
    response_data = handle_row(data)
    if response_data is None:
        raise HTTPException(409, "Action not valid for given state")
    return JSONResponse(response_data)


@app.post("/ring", response_class=JSONResponse)
async def ring(request: Request):
    data = await request.json()
    response_data = handle_ring(*parse_data(data))
    if response_data is None:
        raise HTTPException(409, "Action not valid for given state")
    return JSONResponse(response_data)


@app.post("/outcome", response_class=JSONResponse)
async def outcome(request: Request):
    data = await request.json()
    _, game = parse_data(data)
    response_data = get_outcome(game)
    if response_data is None:
        raise HTTPException(409, "Game not over")
    return JSONResponse(response_data)
