import os
import sys

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from flask import Flask, jsonify,request
from flask_cors import CORS

from llm.generate_recipes import GenerateRecipes
from neo4j import GraphDatabase
import neo4j




app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
#CORS(app)  # Enable CORS for all routes


@app.route('/', methods=['GET'])
def index():
    data = {"message": "Recipes Generator!"}
    return jsonify(data)

@app.route('/api/submit-text', methods=['POST', 'OPTIONS'])
def generate_response():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    data = request.json
    
    user_text = data.get('text', '').strip()

    #generate_recipes = GenerateRecipes()
    #recipes_json =  generate_recipes.generate(user_text)
    
    # For testing
    #
    # That is the respond I'm waiting for
    recipes_json = [
                    {'receta': 'Tortilla de patatas',
                    'ingredientes': [
                    {'ingrediente':'Huevos','categoria': 'Huevos grandes', 'qty': 4, 'unit': 'unidades'},
                    {'ingrediente':'Cebolla', 'categoria': 'Cebolla y ajo', 'qty': 1, 'unit': 'unidad'},
                    {'ingrediente':'Aceite','categoria': 'Aceite de oliva virgen y virgen extra', 'qty': 100, 'unit': 'ml'},
                    {'ingrediente':'Sal','categoria': 'Sal y bicarbonato', 'qty': 1, 'unit': 'pizca'},
                    ]
                },
            ]

     # Check if user_text is empty and respond accordingly
    if not user_text:
        return jsonify({"error": "No text provided"}), 400
    
    # Process user_text using your logic here
    recipes = {"message": recipes_json}
    return jsonify(recipes)

if __name__ == '__main__':
    app.run(debug=True)
