from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
import chess

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Initialize the chess board
board = chess.Board()

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "fen": board.fen()})

@app.post("/move")
async def make_move(request: Request):
    data = await request.json()
    move = chess.Move.from_uci(data['move'])
    if move in board.legal_moves:
        board.push(move)
        return JSONResponse(content={"fen": board.fen(), "status": "success"})
    return JSONResponse(content={"status": "error", "message": "Illegal move"})

@app.get("/reset")
async def reset_game():
    global board
    board = chess.Board()
    return JSONResponse(content={"fen": board.fen(), "status": "success"})