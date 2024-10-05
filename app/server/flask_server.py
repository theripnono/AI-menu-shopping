import os
import sys
import json
from .search_products import procces_recipes


# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from flask import Flask, jsonify,request
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
#CORS(app)  # Enable CORS for all routes

def test_neo4j():
    with open('exported_data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

@app.route('/', methods=['GET'])
def index():
    data = {"message": "Generador de Recetas"}
    return jsonify(data)


@app.route('/api/submit-text', methods=['POST', 'OPTIONS'])
def generate_response():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    data = request.json
    
    user_text = data.get('text', '').strip()

    
    recipes_json =  procces_recipes(user_text)
    
    # For testing
    # That is the respond I'm waiting for
    #recipes_json = test_neo4j()

    # Check if user_text is empty and respond accordingly
    if not user_text:
        return jsonify({"error": "No text provided"}), 400
    
    # Process user_text using your logic here
    print(recipes_json)

    recipes = {"message": recipes_json}
    return jsonify(recipes)

if __name__ == '__main__':
    app.run(debug=True)
