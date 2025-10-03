from dotenv import load_dotenv
from app import create_app

# Load env
load_dotenv()

app = create_app()
if __name__ == "__main__":   
    app.run(debug=True,port=5500)
