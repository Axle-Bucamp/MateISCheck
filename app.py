from flask import Flask, jsonify
import chess

app = Flask(__name__)
board = chess.Board()

@app.route('/test', methods=['GET'])
def test_route():
    return jsonify({"message": "Chess API is working!"}), 200

@app.route('/board', methods=['GET'])
def get_board():
    return jsonify({"board": board.fen()}), 200

if __name__ == '__main__':
    app.run(debug=True)