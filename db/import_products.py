from neo4j import GraphDatabase
from dotenv import dotenv_values
import json
import ast


config = dotenv_values("./.conf")

URI = config['URI']
AUTH = ast.literal_eval(config['AUTH'])

def load_into_graph(nodes:list[dict]):

    """
    Load formated rows into neo4j db.

    :param nodes: list of nodes.

    e.g:
    """

    try:
        with GraphDatabase.driver(URI, auth=AUTH) as driver:
            driver.verify_connectivity()
            session = driver.session()

            print("Importing data to the graph. Please wait...")

            """
            change the item structure
            data = [{
                "Ternera": {
                    "product_id": 4199,
                    "product_ean": "20269593",
                    "product_seo": "carrilleras-de-ternera-500-g-aprox",
                    "product_name": "Carrilleras de ternera (500 g aprox)",
                    "product_brand": " ",
                    "product_price_centAmount": 16.98,
                    "product_price_centUnitAmount": 16.98,
                    "product_offer_price_centAmount": None,
                    "product_offer_price_centUnitAmount": None
                }
            },
            ]
            """
            items = []
            for node in nodes:
                for category, product_info in node.items():
                    product_info["category"] = category
                    items.append(product_info)

            query = """
                UNWIND $items AS item
                MERGE (c:Category {category: item.category})
                MERGE (p:Product {product_id: item.product_id})
                MERGE (c)<-[:BELONGS]-(p)
                SET p.product_ean = item.product_ean,
                    p.product_seo = item.product_seo,
                    p.product_name = item.product_name,
                    p.product_brand = item.product_brand,
                    p.product_img = item.product_img,
                    p.product_price_centAmount = item.product_price_centAmount,
                    p.product_price_centUnitAmount = item.product_price_centUnitAmount,
                    p.product_offer_price_centAmount = item.product_offer_price_centAmount,
                    p.product_offer_price_centUnitAmount = item.product_offer_price_centUnitAmount
            """

            # Run the query with the items as parameters
            session.run(query, items=items)


                
        print("All nodes has been succesfully created")

    except Exception as e:
        print('Oups! something goes wrong, please check: ')
        print({e})


def import_data(file:str)->list[dict]:
    
    # Read the JSON file
    with open(file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    return data

input_file = 'db/demo/products.json'
nodes = import_data(input_file) 
load_into_graph(nodes)

