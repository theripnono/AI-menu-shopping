from neo4j import GraphDatabase
from dotenv import dotenv_values
import json
import ast
import hashlib

"""
Import demo users to de db
"""

config = dotenv_values("./.conf")

URI = config['URI']
AUTH = ast.literal_eval(config['AUTH'])




def load_into_graph(nodes:list[dict]):

    """
    Load formated rows into neo4j db.
    :param nodes: list of nodes.
    """

    try:
        with GraphDatabase.driver(URI, auth=AUTH) as driver:
            driver.verify_connectivity()
            session = driver.session()

            print("Importing demo users to the graph. Please wait...")

            #TODO use encript function for the anonimation of the nodes.
            
            """
            change the item structure
            data =[
                    {"nombre": "Admin", "id_cliente": 123456, "fcliente": "20/05/2003", "edad": 28, "sexo": "M", "ciudad": "Bilbao"},
                    {"nombre": "Ana",   "id_cliente": 556644, "fcliente": "05/10/2012", "edad": 34, "sexo": "F", "ciudad": "Irun"},
                    {"nombre": "David", "id_cliente": 789310, "fcliente": "19/03/2019", "edad": 22, "sexo": "M", "ciudad": "Irun"},
                    {"nombre": "Lucía", "id_cliente": 492513, "fcliente": "06/02/2022", "edad": 30, "sexo": "F", "ciudad": "Donosti"},
                    {"nombre": "Jorge", "id_cliente": 987314, "fcliente": "16/05/20012", "edad": 25, "sexo": "M", "ciudad": "Bilbao"}
                ]
            """

            query = """
                UNWIND $items AS item
                MERGE (u:User {name: item.nombre})
                SET u.edad = item.edad,
                    u.id_cliente=item.id_cliente,
                    u.fecha_alta_cliente = item.fcliente,
                    u.sexo = item.sexo,
                    u.ciudad = item.ciudad,
                 
            """

            # Run the query with the items as parameters
            session.run(query, items=nodes)
               
        print("All nodes has been succesfully created")

    except Exception as e:
        print('Oups! something goes wrong, please check: ')
        print({e})


def encrypt_users(user:str):
    md5 = hashlib.md5(user.encode())
    return md5.hexdigest() 

def import_data(file:str)->list[dict]:
    
    # Read the JSON file
    with open(file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    return data

input_file = 'db/users.json'
nodes = import_data(input_file) 
load_into_graph(nodes)

