from .generate_recipes import GenerateRecipes
from neo4j import GraphDatabase
import neo4j
from dotenv import dotenv_values
import json
import ast
from datetime import datetime

config = dotenv_values(".conf")

URI = config['URI']
AUTH = ast.literal_eval(config['AUTH'])


"""

Probar en local sin serv ni app
"""


# For testing
# That is the respond I'm waiting for
def export_json(df:object)->object:

    """
    df input estructure example:
                                            name            brand  ...  cantidad      unit
       0                          Huevos L docena    Gorrotxategi  ...         4  unidades
       1                 Huevos L de suelo docena            Dagu  ...         4  unidades
       2                      Huevos L 1/2 docena              BM  ...         4  unidades
       3                      Huevos L 1/2 docena    Gorrotxategi  ...         4  unidades
       4                 Huevos euskolabel decena     Eusko Label  ...         4  unidades
       5                          Huevos L docena              BM  ...         4  unidades
       6  Cebolla ecológica en malla (1 kg aprox)             ...  ...         1    unidad
       7                Cebolla tubo (1 kg aprox)             ...  ...         1    unida
    
    This functions generates a json file that will be displayed in the frontend.

    """

    recetas_json = []

    # group by recipes
    grouped = df.groupby('receta')
    for receta, group in grouped:
        receta_dict = {
            'receta': receta,
            'ingredientes': {}
        }
        
        # Agrupar por ingrediente dentro de cada receta
        for _, row in group.iterrows():
            ingrediente = row['ingrediente']
            
            # Crear el diccionario del ingrediente si no existe
            if ingrediente not in receta_dict['ingredientes']:
                receta_dict['ingredientes'][ingrediente] = {
                    'nombre': ingrediente,
                    'quantity': row['cantidad'],
                    'unit': row['unit'],
                    'productos': []
                }
            
            # Añadir el producto a la lista de productos
            producto_info = {
                'product_name': row['name'],
                'product_id':row['pid'],
                'product_brand': row['brand'].strip(),
                'price': row['price'],
                'img': row['img']

            }
            receta_dict['ingredientes'][ingrediente]['productos'].append(producto_info)
        
        recetas_json.append(receta_dict)

    print("recipes files was sucesfully generated")
    return recetas_json


def procces_recipes(user_input):
    
    """
    Process the llm output and get the products from neo4j db
    """

    recipe_obj = GenerateRecipes()
    response_recipes = recipe_obj.generate(user_input)
    try:
        with GraphDatabase.driver(URI, auth=AUTH) as driver:
            driver.verify_connectivity()

            records_df = driver.execute_query(
                "UNWIND $response_recipes as receta "
                "UNWIND receta.ingredientes as ingrediente "
                "MATCH (c:Category {category: ingrediente.categoria})--(p:Product) "
                "RETURN p.product_name as name, "
                "p.product_brand as brand, "
                "p.product_price_centAmount as price,"
                "p.product_img as img,"
                "p.product_id as pid,"
                "receta.receta as receta,"
                "ingrediente.ingrediente as ingrediente,"
                "ingrediente.qty as cantidad,"
                "ingrediente.unit as unit"
                        
                , response_recipes=response_recipes
                , database_="neo4j"
                , result_transformer_=neo4j.Result.to_df
            )

        json_export = export_json(records_df)

        # Store a json copy of the neo4j output 
        current_datetime = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_name = f'neo4j_outputs/{current_datetime}_output_data_.json'

        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(json_export, file, indent=4, ensure_ascii=False)
        
        return json_export
    
    except Exception as e:
        print('Oups! something goes wrong, please check: ')
        print({e})