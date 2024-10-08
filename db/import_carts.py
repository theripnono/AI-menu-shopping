from neo4j import GraphDatabase
from dotenv import dotenv_values
import json
import ast
import hashlib

"""
Import demo carts to de db

When the users create the cart import the data from the frontend.
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

            print("Importing demo carts to the graph. Please wait...")

            """
            Node structure:
            data= [
                'cart':cart_id,
                'id_cliente':id_cliente,
                'products'=[
                    {'product_id':product_id},
                    {'product_id':product_id},
                    {'product_id':product_id},
                    {'product_id':product_id},
                ]
            ]
                     1  n         1   n 
            (user_id) -> (cart_id) -> (product_id)
            https://community.neo4j.com/t/creating-a-relationship-between-2-nodes/38408/2
            """

            query = """
                UNWIND $items AS item
                MERGE (c:Cart{cart_id:item.card_id})
                SET c.id_cliente=item.id_cliente,
                    c.products=item.products
                
                MATCH (c:Cart),(u.User)
                WHERE c.id_cliente = u.id_cliente
                CREATE (u)-[:ha_comprado]->(c);
            """

            # Run the query with the items as parameters
            session.run(query, items=nodes)
               
        print("All nodes has been succesfully created")

    except Exception as e:
        print('Oups! something goes wrong, please check: ')
        print({e})


def import_data(file:str)->list[dict]:
    # Read the JSON file
    with open(file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    return data

input_file = 'db/cart.json'
nodes = import_data(input_file) 
load_into_graph(nodes)

