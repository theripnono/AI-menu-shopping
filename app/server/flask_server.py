import os
import sys

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from flask import Flask
from llm.generate_recipes import GenerateRecipes

from flask import Flask
from neo4j import GraphDatabase
import neo4j


app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello-World!</p>"
