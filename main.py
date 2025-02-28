from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import chess

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

board = chess.Board()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "fen": board.fen()})

@app.post("/move")
async def make_move(move: str):
    try:
        chess_move = chess.Move.from_uci(move)
        if chess_move in board.legal_moves:
            board.push(chess_move)
            return {"status": "success", "fen": board.fen()}
        else:
            return {"status": "error", "message": "Illegal move"}
    except ValueError:
        return {"status": "error", "message": "Invalid move format"}

@app.get("/reset")
async def reset_game():
    global board
    board = chess.Board()
    return {"status": "success", "fen": board.fen()}
