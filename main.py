from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import chess

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Initialize the chess board
board = chess.Board()

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("chessboard.html", {"request": request, "fen": board.fen()})

@app.post("/move/{move}")
async def make_move(move: str):
    try:
        board.push_san(move)
        return {"success": True, "fen": board.fen(), "is_game_over": board.is_game_over()}
    except ValueError:
        return {"success": False, "error": "Invalid move"}

@app.get("/reset")
async def reset_board():
    global board
    board = chess.Board()
    return {"success": True, "fen": board.fen()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)