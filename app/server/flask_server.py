import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from llm.generate_recipes import _generate_recipes
from neo4j import GraphDatabase
import neo4j


app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello-World!</p>"

def printa():
    return "<p>printa algo</p>"