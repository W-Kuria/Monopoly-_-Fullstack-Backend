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

    # Create game
    new_game = Game(player_count=num_players, created_by=user_id, status="active", current_turn=0)
    db.session.add(new_game)
    db.session.commit()  # to get new_game.id

    # Add players
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

    # Initialize game board tiles for this game (clone static board)
    static_tiles = Board.query.all()
    for tile in static_tiles:
        game_tile = GameBoardTile(
            game_id=new_game.id,
            board_id=tile.id,
            owner_id=None,
            mortgaged=False
        )
        db.session.add(game_tile)
    db.session.commit()

    # Set the first player’s turn
    if players:
        new_game.current_turn = players[0].id
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
        "player_count": game.player_count,
        "current_turn": game.current_turn,
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

    if game.current_turn != player.id:
        return jsonify({"error": "It's not your turn"}), 403

    dice1, dice2 = random.randint(1, 6), random.randint(1, 6)
    move = dice1 + dice2

    old_position = player.position
    new_position = (old_position + move) % 40

    # Check laps for passing GO
    if new_position < old_position:
        player.laps += 1
        player.money += 200

    player.position = new_position

    # Determine next player turn
    players = Player.query.filter_by(game_id=game.id).order_by(Player.id).all()
    current_index = next((i for i, p in enumerate(players) if p.id == player.id), 0)
    next_index = (current_index + 1) % len(players)
    next_player = players[next_index]

    game.current_turn = next_player.id
    db.session.commit()

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


@game_bp.route("/games/<int:game_id>/board", methods=["GET"])
def get_board(game_id):
    game_tiles = GameBoardTile.query.filter_by(game_id=game_id).join(Board).order_by(Board.position.asc()).all()
    return jsonify([
        {
            "id": t.board.id,
            "name": t.board.name,
            "position": t.board.position,
            "type": t.board.type,
            "price": t.board.price,
            "rent": t.board.rent,
            "owner_id": t.owner_id,
            "mortgaged": t.mortgaged
        }
        for t in game_tiles
    ])



@game_bp.route("/<int:game_id>/buy", methods=["POST"])
def buy_property(game_id):
    data = request.get_json()
    player_id = data.get("player_id")
    tile_position = data.get("tile_position")

    player = Player.query.filter_by(id=player_id, game_id=game_id).first()
    if not player:
        return jsonify({"error": "Player not found"}), 404

    game = Game.query.get(game_id)
    if game.current_turn != player.id:
        return jsonify({"error": "It's not your turn"}), 403

    game_tile = GameBoardTile.query.filter_by(game_id=game_id).join(Board).filter(Board.position == tile_position).first()
    if not game_tile:
        return jsonify({"error": "Tile not found"}), 404

    if game_tile.owner_id is not None:
        return jsonify({"error": "Property already owned"}), 400

    if game_tile.board.type != "property":
        return jsonify({"error": "This tile is not a property"}), 400

    price = game_tile.board.price
    if player.money < price:
        return jsonify({"error": "Not enough money"}), 400

    player.money -= price
    game_tile.owner_id = player.id
    db.session.commit()

    return jsonify({
        "message": f"{player.name} bought {game_tile.board.name} for ${price}",
        "player_money": player.money
    })


@game_bp.route("/<int:game_id>/chance", methods=["POST"])
def draw_chance(game_id):
    player_id = request.json.get("player_id")
    player = Player.query.filter_by(id=player_id, game_id=game_id).first()
    if not player:
        return jsonify({"error": "Player not found"}), 404

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
        player.in_jail = True
        player.jail_turns = 0

    db.session.commit()

    return jsonify({"card": log, "player": {
        "id": player.id, "money": player.money, "position": player.position
    }})


@game_bp.route("/<int:game_id>/community", methods=["POST"])
def draw_community(game_id):
    player_id = request.json.get("player_id")
    player = Player.query.filter_by(id=player_id, game_id=game_id).first()
    if not player:
        return jsonify({"error": "Player not found"}), 404

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
        player.in_jail = True
        player.jail_turns = 0

    db.session.commit()

    return jsonify({"card": log, "player": {
        "id": player.id, "money": player.money, "position": player.position
    }})


@game_bp.route("/<int:game_id>/jail", methods=["POST"])
def handle_jail(game_id):
    data = request.get_json()
    player_id = data.get("player_id")
    action = data.get("action")  # 'pay', 'skip', 'card'

    player = Player.query.filter_by(id=player_id, game_id=game_id).first()
    if not player:
        return jsonify({"error": "Player not found"}), 404

    if not player.in_jail:
        return jsonify({"error": "Player is not in jail"}), 400

    if action == "pay":
        if player.money >= 50:
            player.money -= 50
            player.in_jail = False
            player.jail_turns = 0
            db.session.commit()
            return jsonify({"message": "Paid $50 and released", "player": {"money": player.money}})
        return jsonify({"error": "Not enough money"}), 400

    elif action == "skip":
        player.jail_turns += 1
        # If player skips 3 turns, automatically release (optional)
        if player.jail_turns >= 3:
            player.in_jail = False
            player.jail_turns = 0
            db.session.commit()
            return jsonify({"message": "Released after 3 turns in jail"})
        db.session.commit()
        return jsonify({"message": f"Skipped turn {player.jail_turns} in jail"})

    elif action == "card":
        # Assume player has 'Get out of jail' card logic elsewhere
        player.in_jail = False
        player.jail_turns = 0
        db.session.commit()
        return jsonify({"message": "Used card to get out of jail"})

    return jsonify({"error": "Invalid action"}), 400


@game_bp.route("/<int:game_id>/rent", methods=["POST"])
def pay_rent(game_id):
    data = request.get_json()
    player_id = data.get("player_id")
    tile_position = data.get("tile_position")

    player = Player.query.filter_by(id=player_id, game_id=game_id).first()
    if not player:
        return jsonify({"error": "Player not found"}), 404

    game_tile = GameBoardTile.query.filter_by(game_id=game_id).join(Board).filter(Board.position == tile_position).first()
    if not game_tile or not game_tile.owner_id:
        return jsonify({"error": "Property not owned"}), 400

    if game_tile.owner_id == player.id:
        return jsonify({"error": "Cannot pay rent to yourself"}), 400

    owner = Player.query.get(game_tile.owner_id)
    rent = game_tile.board.rent

    if player.money < rent:
        return jsonify({"error": "Insufficient funds to pay rent"}), 400

    player.money -= rent
    owner.money += rent

    db.session.commit()

    return jsonify({
        "message": f"{player.name} paid ${rent} rent to {owner.name}",
        "player_money": player.money,
        "owner_money": owner.money
    })
