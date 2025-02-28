from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from chess_game import ChessGame

app = FastAPI()
templates = Jinja2Templates(directory="templates")

chess_game = ChessGame()

class Move(BaseModel):
    from_square: str
    to_square: str

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "board": chess_game.get_board()})

@app.post("/move")
async def make_move(move: Move):
    result = chess_game.make_move(move.from_square, move.to_square)
    return {"success": result, "board": chess_game.get_board()}

@app.get("/reset")
async def reset_game():
    chess_game.reset()
    return {"message": "Game reset", "board": chess_game.get_board()}