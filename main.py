from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import chess

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

board = chess.Board()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "fen": board.fen()})

@app.post("/move")
async def make_move(from_square: str, to_square: str):
    move = chess.Move.from_uci(from_square + to_square)
    if move in board.legal_moves:
        board.push(move)
        return {"success": True, "fen": board.fen()}
    return {"success": False, "message": "Illegal move"}

@app.get("/reset")
async def reset_game():
    global board
    board = chess.Board()
    return {"success": True, "fen": board.fen()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)