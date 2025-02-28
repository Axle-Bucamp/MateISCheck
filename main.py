from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import chess

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/move")
async def generate_move(fen: str):
    try:
        board = chess.Board(fen)
        moves = list(board.legal_moves)
        return {"moves": [str(move) for move in moves]}
    except Exception as e:
        return {"error": str(e)}

@app.post("/validate-move")
async def validate_move(fen: str, move: str):
    try:
        board = chess.Board(fen)
        chess_move = chess.Move.from_uci(move)
        is_valid = chess_move in board.legal_moves
        return {"isValid": is_valid}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)