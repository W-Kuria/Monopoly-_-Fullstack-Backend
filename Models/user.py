from Models import db

# -----------------------------
# Users who can create/join games
# -----------------------------
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    # A user can create many games
    games = db.relationship("Game", back_populates="creator")


# -----------------------------
# Game sessions
# -----------------------------
class Game(db.Model):
    __tablename__ = "games"

    id = db.Column(db.Integer, primary_key=True)
    player_count = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    status = db.Column(db.String, default="active")  # active, finished
    current_turn = db.Column(db.Integer, default=0)  # which player's turn
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # relationships
    creator = db.relationship("User", back_populates="games")
    players = db.relationship("Player", back_populates="game", cascade="all, delete-orphan")
    board_tiles = db.relationship("GameBoardTile", back_populates="game", cascade="all, delete-orphan")


# -----------------------------
# Players inside each game
# -----------------------------
class Player(db.Model):
    __tablename__ = "players"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    money = db.Column(db.Integer, default=1500)
    position = db.Column(db.Integer, default=0)
    in_jail = db.Column(db.Boolean, default=False)
    jail_turns = db.Column(db.Integer, default=0)
    laps = db.Column(db.Integer, default=0)

    game_id = db.Column(db.Integer, db.ForeignKey("games.id"), nullable=False)
    game = db.relationship("Game", back_populates="players")


# -----------------------------
# Static Monopoly board template
# (40 spaces: Go, Properties, Jail, etc.)
# -----------------------------
class Board(db.Model):
    __tablename__ = "board"

    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)  # property, chance, tax, go, jail, etc.

    # extra info for property-type spaces
    price = db.Column(db.Integer)
    rent = db.Column(db.Integer)


# -----------------------------
# Per-game copy of board spaces
# -----------------------------
class GameBoardTile(db.Model):
    __tablename__ = "game_board_tiles"

    id = db.Column(db.Integer, primary_key=True)

    game_id = db.Column(db.Integer, db.ForeignKey("games.id"), nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey("board.id"), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("players.id"), nullable=True)

    mortgaged = db.Column(db.Boolean, default=False)

    # relationships
    game = db.relationship("Game", back_populates="board_tiles")
    board = db.relationship("Board")
    owner = db.relationship("Player")


# -----------------------------
# Chance & Community Chest
# -----------------------------
class ChanceCard(db.Model):
    __tablename__ = "chance_cards"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)


class CommunityChestCard(db.Model):
    __tablename__ = "community_chest_cards"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)


# -----------------------------
# Optional: Log actions/events
# -----------------------------
class ActionLog(db.Model):
    __tablename__ = "action_logs"

    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey("games.id"), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey("players.id"))
    action = db.Column(db.String, nullable=False)  # "rolled dice", "bought property", etc.
    amount = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())