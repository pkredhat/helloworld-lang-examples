from flask import Blueprint, jsonify, request, abort
import json
import os

main = Blueprint('main', __name__)

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

@main.route("/", methods=["GET"])
def index():
    country_code = os.getenv("COUNTRY_CODE", "en")

    try:
        translation = get_translation(country_code)
    except Exception as e:
        abort(500, description=str(e))

    return jsonify({"translation": translation}), 200

# @main.route("/query", methods=["GET"])
# def query_translation():
#     code = request.args.get("cc")
#     if not code:
#         abort(400, description="Missing 'cc' query parameter.")

#     try:
#         translation = get_translation(code)
#     except Exception as e:
#         abort(500, description=str(e))

#     return jsonify({"translation": translation}), 200