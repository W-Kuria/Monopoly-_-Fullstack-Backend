from app.db import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.String(255), nullable=True)

class Player(db.Model):
    __tablename__ = "players"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    money = db.Column(db.Integer, default=1500)
    position = db.Column(db.Integer, default=0)
    in_jail = db.Column(db.Boolean, default=False)
    board_id = db.Column(db.Integer, db.ForeignKey("board.id"))
    laps = db.Column(db.Integer, default=0)


class Property(db.Model):
    __tablename__ = "properties"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    price = db.Column(db.Integer, nullable=True)
    position = db.Column(db.Integer, nullable=True, unique=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    rent = db.Column(db.Integer, nullable=True)

class ChanceCard(db.Model):
    __tablename__ = "chance_cards"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)

class CommunityChestCard(db.Model):
    __tablename__ = "community_chest_cards"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)

class Board(db.Model):
    __tablename__ = "board"
    id = db.Column(db.Integer, primary_key=True)  
    position = db.Column(db.Integer, unique=True, nullable=True)
    name = db.Column(db.String, nullable=True)
    type = db.Column(db.String) 