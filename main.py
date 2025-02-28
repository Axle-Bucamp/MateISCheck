from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from chess_engine import ChessGame

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Initialize chess game
chess_game = ChessGame()

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("chess.html", {"request": request, "board": chess_game.get_board()})

@app.post("/move")
async def make_move(from_square: str, to_square: str):
    success = chess_game.make_move(from_square, to_square)
    return {"success": success, "board": chess_game.get_board()}

@app.get("/reset")
async def reset_game():
    chess_game.reset()
    return {"message": "Game reset", "board": chess_game.get_board()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)