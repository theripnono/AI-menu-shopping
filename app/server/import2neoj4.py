from neo4j import GraphDatabase
from dotenv import dotenv_values
import json
import ast
import hashlib
import secrets

from datetime import datetime

"""
Import data to neo4j db

When the users create the cart import the data from the frontend.
"""

config = dotenv_values("./.conf")

URI = config['URI']
AUTH = ast.literal_eval(config['AUTH'])




# TODO 
# User sesion


def _create_cart_id():
    token = secrets.token_bytes(10) 
    result = hashlib.md5(token)
    return result.hexdigest()

def _purchased_query(user_sesion:str, order:list[dict]):
            
    """
    Import the purchased order.
    params:
        user: The user session
    """

    order_id = _create_cart_id()
    
    #id_cliente = user_sesion
    name= user_sesion
    now = datetime.now()
    purchased_date =  now.strftime("%m/%d/%Y, %H:%M:%S")
    products_id = [{'product_id':product_line['product']['product_id'],
                    'quantity':product_line['quantity']} for product_line in order]
    
    order_bill=sum([product_line['product']['price'] for product_line in order])


    query = """
    MERGE (o:Order {order_id: $order_id, purchased_date: $purchased_date, order_bill: $order_bill})
    
    WITH o
    MATCH (u:User {name: $name})
    CREATE (u)-[:HA_COMPRADO]->(o)

    WITH o
    UNWIND $products_id as product_id
    MATCH (p:Product {product_id: product_id.product_id})
    CREATE (o)-[:contiene {cantidad:product_id.quantity}]->(p)
    """

    parameters = {
        "order_id": order_id,
        "purchased_date": purchased_date,
        "order_bill":order_bill,
        "products_id":products_id,
        "name": name
        
    }

    load_into_graph(query, parameters)
        
    print(f'the {order_id} node was created')
    

def load_into_graph(query:str, parameters:dict):

    """
    Load formated rows into neo4j db.
    :param nodes: list of nodes.
    """


    try:
        with GraphDatabase.driver(URI, auth=AUTH) as driver:
            driver.verify_connectivity()
            session = driver.session()
            session.run(query, parameters=parameters)       
        print("All nodes has been succesfully created")

    except Exception as e:
        print('Oups! something goes wrong, please check: ')
        print({e})



test_nodes = [{'product':
                {'img': 'https://cdn-bm.aktiosdigitalservices.com/tol/bm/media/product/img/300x300/A16983_00.jpg?t=20241003030611',
                'price': 1.99,
                'product_brand': 'Buti',
                'product_id': 4435,
                'product_name': 'Cebolla roja (700 g aprox)'},
                'quantity': 1
                },
                {'product': {'img': 'https://cdn-bm.aktiosdigitalservices.com/tol/bm/media/product/img/300x300/A74147_00.jpg?t=20241004030319',
                'price': 9.7,
                'product_brand': 'Trujal Almazara',
                'product_id': 42,
                'product_name': 'Aceite de oliva virgen extra Tudela 1 l'},
                'quantity': 2}
                
            ]
