from flask import Flask
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Register routes
from routes.main import main as main_blueprint
app.register_blueprint(main_blueprint)

PORT = int(os.getenv("PORT", "3000"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)