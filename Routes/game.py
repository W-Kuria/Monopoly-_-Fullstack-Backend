from flask import Blueprint, request, jsonify
from app import db
from Models.user import *
import random

game_bp = Blueprint("game", __name__, url_prefix="/game")

@game_bp.route("/create", methods=["POST"])
def create_game():
    data = request.get_json()
    num_players = data.get("num_players")
    player_names = data.get("players", [])
    user_id = data.get("userId")  # track creator

    if not num_players or num_players < 2 or num_players > 4:
        return jsonify({"error": "Invalid number of players"}), 400

    if len(player_names) != num_players:
        return jsonify({"error": "Player names must match number of players"}), 400

    # ✅ Create game
    new_game = Game(player_count=num_players, created_by=user_id, status="active")
    db.session.add(new_game)
    db.session.commit()  # <-- ensures ID is generated

    # ✅ Add players
    players = []
    for name in player_names:
        p = Player(
            name=name,
            game_id=new_game.id,
            money=1500,
            position=0,
            in_jail=False,
            laps=0
        )
        db.session.add(p)
        players.append(p)

    db.session.commit()

    return jsonify({
    "id": new_game.id,
    "status": new_game.status,
    "player_count": new_game.player_count,
    "players": [{"id": p.id, "name": p.name, "money": p.money} for p in players]
})





@game_bp.route("/<int:game_id>", methods=["GET"])
def get_game_state(game_id):
    game = Game.query.get_or_404(game_id)
    players = [
        {
            "id": p.id,
            "name": p.name,
            "money": p.money,
            "position": p.position,
            "laps": p.laps,
            "in_jail": p.in_jail
        }
        for p in game.players
    ]
    return jsonify({
        "id": game.id,
        "status": game.status,
        "playerCount": game.player_count,
        "players": players
    })


@game_bp.route("/<int:game_id>/roll", methods=["POST"])
def roll_dice(game_id):
    game = Game.query.get_or_404(game_id)
    data = request.get_json()
    player_id = data.get("player_id")

    player = Player.query.filter_by(id=player_id, game_id=game.id).first()
    if not player:
        return jsonify({"error": "Player not found"}), 404

    dice1, dice2 = random.randint(1, 6), random.randint(1, 6)
    move = dice1 + dice2

    new_position = (player.position + move) % 40
    if new_position < player.position:
        player.laps += 1
        player.money += 200  # Passing GO

    player.position = new_position
    db.session.commit()

    return jsonify({
        "dice": [dice1, dice2],
        "player": {
            "id": player.id,
            "position": player.position,
            "laps": player.laps,
            "money": player.money
        }
    })
@game_bp.route("/user/<int:user_id>", methods=["GET"])
def get_user_games(user_id):
    games = Game.query.filter_by(created_by=user_id).all()
    
    return jsonify([
        {
            "id": game.id,
            "status": game.status,
            "player_count": game.player_count,
            "current_turn": game.current_turn,
            "created_at": game.created_at.isoformat() if game.created_at else None
        }
        for game in games
    ])
