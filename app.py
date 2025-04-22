from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from game import LiarsBarRevolver

app = Flask(__name__, static_folder='static')
game = LiarsBarRevolver()

# Get the base URL from environment variable or use default
BASE_URL = os.environ.get('BASE_URL', '')

@app.route('/')
def home():
    return render_template('index.html', base_url=BASE_URL)

@app.route('/manifest.json')
def manifest():
    return send_from_directory('static', 'manifest.json')

@app.route('/sw.js')
def service_worker():
    return send_from_directory('static', 'sw.js')

@app.route('/static/icons/<path:filename>')
def serve_icon(filename):
    return send_from_directory('static/icons', filename)

@app.route('/select_table', methods=['POST'])
def select_table():
    table = game.select_random_table()
    return jsonify({"table": table})

@app.route('/add_player', methods=['POST'])
def add_player():
    name = request.json.get('name')
    success, message = game.add_player(name)
    return jsonify({"success": success, "message": message})

@app.route('/select_player', methods=['POST'])
def select_player():
    name = request.json.get('name')
    success, message = game.select_player(name)
    return jsonify({"success": success, "message": message})

@app.route('/shoot', methods=['POST'])
def shoot():
    player_name = request.json.get('player_name')
    result = game.shoot(player_name)
    return jsonify(result)

@app.route('/reset', methods=['POST'])
def reset():
    chambers = request.json.get('chambers', 6)
    game.reset_game(chambers)
    return jsonify({"success": True, "message": "Game reset"})

@app.route('/reset_scoreboard', methods=['POST'])
def reset_scoreboard():
    message = game.reset_scoreboard()
    return jsonify({"success": True, "message": message})

@app.route('/spin', methods=['POST'])
def spin():
    success, message = game.spin()
    return jsonify({"success": success, "message": message})

@app.route('/scores')
def get_scores():
    return jsonify(game.get_scores())

@app.route('/game_state')
def get_game_state():
    return jsonify(game.get_game_state())

@app.route('/previous_players')
def get_previous_players():
    return jsonify(game.get_previous_players())

if __name__ == '__main__':
    app.run(debug=True) 