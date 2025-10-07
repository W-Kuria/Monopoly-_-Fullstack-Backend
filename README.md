# 🏠 Monopoly Fullstack Backend

This is the **backend server** for the Monopoly Fullstack game project. It provides all API endpoints, database management, and game logic for a fully functional digital version of Monopoly. The backend is built with **Flask** and designed to work seamlessly with a React frontend.

---

## 🚀 Features

- **Game Management:** Create, join, and manage Monopoly game sessions.  
- **Player Handling:** Add, remove, and update players, including turn order and jail logic.  
- **Board Logic:** Handles all major tiles like properties, Chance, Community Chest, Go, Jail, and Free Parking.  
- **Property Ownership & Rent:** Buy, sell, and collect rent from owned properties.  
- **Chance & Community Chest:** Draw random cards and trigger their effects.  
- **Jail System:** Pay bail, use a “Get Out of Jail” card, or skip turns.  
- **Bankruptcy Detection:** Automatically removes bankrupt players.  
- **Persistent Storage:** Uses an SQL database for storing games, players, and properties.  

---

## 🧩 Tech Stack

| Component | Technology |
|------------|-------------|
| Backend Framework | Flask (Python) |
| Database | SQLite / PostgreSQL |
| ORM | SQLAlchemy |
| Environment Management | Pipenv |
| API Testing | Postman / Flask test client |
| Version Control | Git + GitHub |

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/monopoly-fullstack-backend.git
cd monopoly-fullstack-backend
```

### 2. Create a Virtual Environment
```bash
pipenv install
pipenv shell
```

### 3. Configure Environment Variables
Create a .env file in the project root and add:

ini
Copy code:
FLASK_ENV=development
DATABASE_URL=sqlite:///monopoly.db
SECRET_KEY=your_secret_key

### 4. Initialize the Database
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 5. Run the Server
```bash
flask run
By default, the API runs at:
http://localhost:5000
```

###  API Endpoints Overview
Method	Endpoint	Description
POST	/game/create	Start a new Monopoly game
POST	/game/<id>/join	Add a player to the game
GET	/game/<id>	Fetch current game state
POST	/game/<id>/move	Move a player after rolling dice
POST	/game/<id>/buy	Buy the property landed on
POST	/game/<id>/rent	Handle rent payment
POST	/game/<id>/chance	Draw a Chance card
POST	/game/<id>/community	Draw a Community Chest card
POST	/game/<id>/jail	Handle jail actions (pay, skip, card)

### Game Logic Highlights
Turn-Based Flow: Each player’s turn automatically rotates after their move.

Randomized Dice Rolls: Dice results are generated securely server-side.

Bank Handling: Rent, taxes, and property costs are tracked in the bank’s balance.

Persistent Sessions: Each game is stored in the database for session recovery.


### 🗂 Folder Structure
```bash

monopoly-fullstack-backend/
│
├── app.py                # Main Flask app entry
├── models/               # SQLAlchemy models
├── routes/               # Blueprint routes (game, player, jail, etc.)
├── migrations/           # Database migrations
├── instance/             # Database instance
├── Pipfile               # Dependencies
├── .env                  # Environment variables
└── README.md             # Project documentation
```

### Contributors
William Kuria and Mathew Kariuki.

and contributors from the Monopoly project team.

