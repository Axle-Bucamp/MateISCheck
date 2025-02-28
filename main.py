from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import chess

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Initialize the chess board
board = chess.Board()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "fen": board.fen()})

@app.post("/move")
async def make_move(from_square: str = Form(...), to_square: str = Form(...)):
    move = chess.Move.from_uci(from_square + to_square)
    if move in board.legal_moves:
        board.push(move)
        return {"status": "success", "fen": board.fen()}
    return {"status": "error", "message": "Illegal move"}

@app.get("/reset")
async def reset_game():
    global board
    board = chess.Board()
    return {"status": "success", "fen": board.fen()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)