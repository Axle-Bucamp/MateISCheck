from flask import Flask, jsonify
import chess

app = Flask(__name__)
board = chess.Board()

@app.route('/test', methods=['GET'])
def test_route():
    return jsonify({"message": "Chess API is working!"})

if __name__ == '__main__':
    app.run(debug=True)