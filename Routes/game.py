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
    data = request.get_json()
    player_id = data.get("player_id")

    game = Game.query.get_or_404(game_id)
    player = Player.query.filter_by(id=player_id, game_id=game.id).first()

    if not player:
        return jsonify({"error": "Player not found"}), 404

    import random
    dice1, dice2 = random.randint(1, 6), random.randint(1, 6)
    move = dice1 + dice2

    # Move player
    old_position = player.position
    new_position = (old_position + move) % 40

    # Passed GO
    if new_position < old_position:
        player.laps += 1
        player.money += 200

    player.position = new_position
    db.session.commit()

    # Return updated data
    game_data = {
        "id": game.id,
        "players": [
            {
                "id": p.id,
                "name": p.name,
                "position": p.position,
                "money": p.money,
                "laps": p.laps,
            } for p in game.players
        ],
        "current_player": {"id": player.id, "name": player.name},
        "dice": [dice1, dice2],
    }

    return jsonify({"message": f"{player.name} rolled {dice1} + {dice2}",
                    "dice": [dice1, dice2],
                    "game": game_data}), 200


    # Determine next player turn
    players = Player.query.filter_by(game_id=game.id).order_by(Player.id).all()
    current_index = next((i for i, p in enumerate(players) if p.id == player.id), 0)
    next_index = (current_index + 1) % len(players)
    next_player = players[next_index]

    # Build response payload
    response = {
        "game_id": game.id,
        "dice": [dice1, dice2],
        "rolled_by": {
            "id": player.id,
            "name": player.name,
            "position": player.position,
            "money": player.money,
            "laps": player.laps
        },
        "next_player": {
            "id": next_player.id,
            "name": next_player.name
        },
        "players": [
            {
                "id": p.id,
                "name": p.name,
                "position": p.position,
                "money": p.money,
                "laps": p.laps
            } for p in players
        ]
    }

    return jsonify(response), 200



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

@game_bp.route("/<int:game_id>/board", methods=["GET"])
def get_board(game_id):
    tiles = Board.query.order_by(Board.position.asc()).all()
    return jsonify([
        {
            "id": t.id,
            "name": t.name,
            "position": t.position,
            "type": t.type,
            "price": t.price,
            "rent": t.rent,
        }
        for t in tiles
    ])

# 💰 Buy property
@game_bp.route("/<int:game_id>/buy", methods=["POST"])
def buy_property(game_id):
    data = request.get_json()
    player_id = data.get("player_id")
    tile_pos = data.get("tile_position")

    player = Player.query.filter_by(id=player_id, game_id=game_id).first()
    tile = Board.query.filter_by(position=tile_pos).first()

    if not tile or tile.type != "property":
        return jsonify({"error": "Not a property"}), 400

    if tile.price > player.money:
        return jsonify({"error": "Not enough money"}), 400

    player.money -= tile.price
    tile.owner_id = player.id  # Add this column in Board model if missing
    db.session.commit()

    return jsonify({
        "message": f"{player.name} bought {tile.name} for ${tile.price}",
        "player_money": player.money
    })


# 🎲 Chance card
@game_bp.route("/<int:game_id>/chance", methods=["POST"])
def draw_chance(game_id):
    player_id = request.json.get("player_id")
    player = Player.query.filter_by(id=player_id, game_id=game_id).first()

    cards = [
        {"message": "Advance to GO! Collect $200", "money": +200, "move": -player.position},
        {"message": "Bank pays you dividend of $50", "money": +50},
        {"message": "Pay school fees of $150", "money": -150},
        {"message": "Go to Jail! Do not pass GO", "jail": True}
    ]

    card = random.choice(cards)
    log = card["message"]

    if "money" in card:
        player.money += card["money"]
    if "move" in card:
        player.position = (player.position + card["move"]) % 40
    if "jail" in card:
        player.position = 10  # Jail position

    db.session.commit()

    return jsonify({"card": log, "player": {
        "id": player.id, "money": player.money, "position": player.position
    }})


# 💳 Community Chest
@game_bp.route("/<int:game_id>/community", methods=["POST"])
def draw_community(game_id):
    player_id = request.json.get("player_id")
    player = Player.query.filter_by(id=player_id, game_id=game_id).first()

    cards = [
        {"message": "You inherit $100", "money": +100},
        {"message": "Pay hospital fees of $100", "money": -100},
        {"message": "From sale of stock you get $50", "money": +50},
        {"message": "Go directly to Jail", "jail": True}
    ]

    card = random.choice(cards)
    log = card["message"]

    if "money" in card:
        player.money += card["money"]
    if "jail" in card:
        player.position = 10  # Jail
    db.session.commit()

    return jsonify({"card": log, "player": {
        "id": player.id, "money": player.money, "position": player.position
    }})


# 🚨 Jail route
@game_bp.route("/<int:game_id>/jail", methods=["POST"])
def handle_jail(game_id):
    data = request.get_json()
    player_id = data.get("player_id")
    action = data.get("action")  # 'pay', 'skip', 'card'
    player = Player.query.filter_by(id=player_id, game_id=game_id).first()

    if action == "pay":
        if player.money >= 50:
            player.money -= 50
            db.session.commit()
            return jsonify({"message": "Paid $50 and released", "player": {"money": player.money}})
        return jsonify({"error": "Not enough money"}), 400

    elif action == "skip":
        # player skips one turn — you could track skipped_turns in the DB
        return jsonify({"message": f"{player.name} skips this turn."})

    elif action == "card":
        return jsonify({"message": f"{player.name} used a Get Out of Jail card!"})

    return jsonify({"error": "Invalid action"}), 400


# 💀 Bankruptcy
@game_bp.route("/<int:game_id>/bankrupt", methods=["POST"])
def bankrupt_player(game_id):
    player_id = request.json.get("player_id")
    player = Player.query.filter_by(id=player_id, game_id=game_id).first()

    player.money = 0
    player.position = -1  # off board
    db.session.commit()

    return jsonify({"message": f"{player.name} is bankrupt and out of the game!"})    

