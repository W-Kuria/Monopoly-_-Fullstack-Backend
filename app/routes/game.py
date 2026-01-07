from flask import Blueprint, request, jsonify
from app import db

game_bp = Blueprint("game", __name__, url_prefix="/game")

@game_bp.route("/create", methods=["POST"])
def create_game():
    return jsonify({"message": "Game created successfully"})

@game_bp.route("/<game_id>/roll-dice", methods=["POST"])
def roll_dice(game_id):
    return jsonify({"message": f"Dice rolled for game {game_id}", "dice": [3, 4]})

@game_bp.route("/<game_id>", methods=["GET"])
def get_game(game_id):
    return jsonify({"game_id": game_id, "status": "active"})

@game_bp.route("/<game_id>/start", methods=["POST", "OPTIONS"])
def start_game(game_id):
    if request.method == "OPTIONS":
        return "", 200
        
    # Update game status from "waiting" to "active"
    return jsonify({
        "message": "Game started!", 
        "game_id": game_id,
        "status": "active",  # Changed from "waiting" to "active"
        "current_player": 1,
        "players": [
            {"id": 1, "name": "Player 1", "position": 0, "money": 1500},
            {"id": 2, "name": "Player 2", "position": 0, "money": 1500}
        ]
    })