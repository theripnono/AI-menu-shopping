from neo4j import GraphDatabase
from dotenv import dotenv_values
import ast
import hashlib
import secrets
import neo4j
from datetime import datetime

"""
Import data to neo4j db

When the users create the cart import the data from the frontend.
When the user save a menu, Menu node + the relation is created
"""

config = dotenv_values("./.conf")

URI = config['URI']
AUTH = ast.literal_eval(config['AUTH'])


# TODO 
# User sesion

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

test_menu = {'ingredientes':
              {'Aceite de oliva virgen extra':
                    {'categoria': 'Aceite de oliva virgen y virgen extra',
                    'nombre': 'Aceite de oliva virgen extra',
                    'productos':
                    [{'img': 'https://cdn-bm.aktiosdigitalservices.com/tol/bm/media/product/img/300x300/A11375_00.jpg?t=20241004030319',
                        'price': 14.18, 'product_brand': 'Maestros de Hojiblanca', 'product_id': 34, 'product_name': 'Aceite de oliva virgen extra 1 l'},
                    {'img': 'https://cdn-bm.aktiosdigitalservices.com/tol/bm/media/product/img/300x300/A11665_00.jpg?t=20241003030006',
                        'price': 13.79, 'product_brand': 'Carbonell', 'product_id': 36, 'product_name': 'Aceite de oliva virgen extra 1 l'}],
            'quantity': 1, 'unit': 'unidad'}},
            'receta': 'Ensalada de quinoa y aguacate'
            }



def _create_token():
    token = secrets.token_bytes(10) 
    result = hashlib.md5(token)
    return result.hexdigest()

def _create_order_node(user_session:str, order:list[dict]):
            
    """
    Import the purchased order to the db
    params:
        user: The user session
    """

    order_id = _create_token()
    
    #id_cliente = user_sesion
    name= user_session
    now = datetime.now()
    purchased_date =  now.strftime("%m/%d/%Y, %H:%M:%S")
    products_id = [{'product_id':product_line['product']['product_id'],
                    'quantity':product_line['quantity']} for product_line in order]
    
    order_bill=sum([product_line['product']['price'] for product_line in order])


    query = """
    MERGE (o:Order {order_id: $order_id, purchased_date: $purchased_date, order_bill: $order_bill})
    
    WITH o
    MATCH (u:User {name: $name})
    CREATE (u)-[:HAS_BUYED]->(o)

    WITH o
    UNWIND $products_id as product_id
    MATCH (p:Product {product_id: product_id.product_id})
    CREATE (o)-[:INCLUDES {cantidad:product_id.quantity}]->(p)
    """

    parameters = {
        "order_id": order_id,
        "purchased_date": purchased_date,
        "order_bill":order_bill,
        "products_id":products_id,
        "name": name   
    }

    connect2_graph(query, parameters)
        
    print(f'the {order_id} node was created')
    
def export_similar_products_json(df:object)->object:

    """
    This function takes the neo4j df output and does the necessary transformations to produce a json
    that will be displayed in the frontend.
    """

    similar_products_json = []
    for _, row in df.iterrows():
        product_info={
            'product_name': row.iloc[0]['product_name'],
            'product_id':row.iloc[0]['product_id'],
            'product_brand': row.iloc[0]['product_brand'].strip(),
            'price': row.iloc[0]['product_price_centAmount'],
            'img': row.iloc[0]['product_img']
        }
        similar_products_json.append(product_info)
       
    return similar_products_json
   

def connect2_graph(query:str, parameters:dict):

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



def similar_products_node():
    # TODO mejorar la query de similar products
    try:
        with GraphDatabase.driver(URI, auth=AUTH) as driver:
            driver.verify_connectivity()
            # TODO descripcion se cambiara por BELONGS
            records_df = driver.execute_query(
                    "MATCH (u:User{name: 'David'})-[:HAS_BUYED]->(o:Order)-[:INCLUDES]->(p1:Product)-[:descripcion]->(c:Category)<-[:descripcion]-(p2:Product)"
                    "WHERE NOT ((u)-[:HAS_BUYED]->(p2))"
                    "RETURN p2"                      
                , database_="neo4j"
                , result_transformer_=neo4j.Result.to_df
            )

        json_export = export_similar_products_json(records_df)
        return json_export
    
    except Exception as e:
        print('Oups! something goes wrong, please check: ')
        print({e})





def _create_menu_node(user_session:str, recipe:dict):


    menu_id = _create_token()
    menu_name = recipe['receta']
    name= user_session
    now = datetime.now()
    date_create_menu =  now.strftime("%m/%d/%Y, %H:%M:%S") # when was the node created

    # Prepare ingredients list for import to neo4j
    ingredientes = []
    for nombre, detalles in recipe['ingredientes'].items():
        ingredientes.append({
            "nombre": nombre,
            "categoria":detalles.get("categoria", ""),
            "quantity": detalles.get("quantity", ""),
            "unit": detalles.get("unit", ""),
            "productos": detalles.get("productos", [])
        })

    query = """
                    MERGE (m:Menu {menu_id: $menu_id})
                    ON CREATE SET m.date_create_menu = $date_create_menu, m.menu_name = $menu_name
                    WITH m

                    MATCH (u:User {name: $name})
                    CREATE (u)-[:HAS_SAVED]->(m)

                    WITH m
                    UNWIND $ingredientes AS ingrediente
                    // Aquí se relaciona con la categoría
                    MATCH (c:Category {category: ingrediente.categoria})  
                    CREATE (m)-[:INCLUDES]->(c)

                """

    parameters = {
        "menu_id":menu_id,
        "menu_name":menu_name,
        "name":name,
        "date_create_menu":date_create_menu,
        "ingredientes": ingredientes,
        }
    
    connect2_graph(query, parameters)
