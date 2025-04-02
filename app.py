from flask import Flask, abort, make_response
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file (if present)
load_dotenv()

app = Flask(__name__)

# Read environment variables
COUNTRY_CODE = os.getenv("COUNTRY_CODE", "en")
PORT = int(os.getenv("PORT", "3000"))

print("countryCode:", COUNTRY_CODE)
print("Port:", PORT)

def get_translation(country_code):
    try:
        with open("translations.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        translations = data.get("translations", {})
        translation = translations.get(country_code.upper())
        if not translation:
            raise Exception("Translation not found for the specified country code.")
        return translation
    except Exception as e:
        raise e

@app.route("/", methods=["GET"])
def index():
    if not COUNTRY_CODE:
        abort(400, description="Country code parameter is required.")
    
    try:
        translation = get_translation(COUNTRY_CODE)
    except Exception as e:
        abort(500, description=str(e))
    
    response = make_response(translation, 200)
    response.headers["Content-Type"] = "text/plain"
    return response

if __name__ == "__main__":
    # Run the Flask server on the port from the environment variable
    app.run(host="0.0.0.0", port=PORT, debug=True)