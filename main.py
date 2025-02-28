from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import chess

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Initialize a new chess board
board = chess.Board()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "fen": board.fen()})

@app.post("/move/")
async def make_move(move: str):
    try:
        chess_move = chess.Move.from_uci(move)
        if chess_move in board.legal_moves:
            board.push(chess_move)
            return {"success": True, "fen": board.fen(), "message": "Move made successfully"}
        else:
            return {"success": False, "message": "Invalid move"}
    except ValueError:
        return {"success": False, "message": "Invalid move format"}

@app.get("/legal_moves/")
async def get_legal_moves():
    return {"moves": [move.uci() for move in board.legal_moves]}

@app.post("/reset/")
async def reset_board():
    global board
    board = chess.Board()
    return {"success": True, "message": "Board reset successfully", "fen": board.fen()}