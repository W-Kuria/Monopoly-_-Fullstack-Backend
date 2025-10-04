from Models import db

class Game(db.Model):
    __tablename__ = "games"

    id = db.Column(db.Integer, primary_key=True)
    player_count = db.Column(db.Integer, nullable=False)  # required
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)  # required
    status = db.Column(db.String, default="active")
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # relationships
    players = db.relationship("Player", back_populates="game", cascade="all, delete-orphan")
