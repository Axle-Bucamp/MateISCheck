from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from chess_logic import ChessGame

app = FastAPI()
templates = Jinja2Templates(directory='templates')
chess_game = ChessGame()

@app.get('/', response_class=HTMLResponse)
async def root(request: Request):
 return templates.TemplateResponse('chessboard.html', {'request': request, 'board': chess_game.board})

@app.post('/move')
async def make_move(from_square: str, to_square: str):
 result = chess_game.make_move(from_square, to_square)
 return {'success': result...