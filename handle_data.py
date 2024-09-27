


"""
delete usless items of the output_ids json
Clean data for a better LLM context

Change some keys
keys of the ouput_ids.json file

# TODO: delete by ids no strings. Changes the items by ids
"""
DELETE_ITEMS=[     'Envasado','Piezas','Infantiles y porciones',
                  'De aquí y de temporada','Calcio y crecimiento',
                  'Sin lactosa y especiales','Condensada, evaporada y en polvo','Batidos y horchata',
                  'Yogur vegetal','Yogur petit e infantil','Yogur bífidus',
                  'Yogur desnatado','Postres lácteos',
                  'Bollería del día','Yogur natural y azucarado',
                  'Yogur sabores','Yogur con frutas','Natillas y crema',
                  'Flan y gelatina','Arroz con leche y cuajada',
                  'Copa y mousse','Tartas','Cápsulas','Natural\r\n',
                  'Descafeinado','Soluble','Mezcla','Grano','Té e infusiones'
                  'Achicoria y cereales solubles','Listo para beber',
                  'Cereales clásicos','Cereales de chocolate','Cereales integrales y dietéticos',
                  'Cereales infantiles','Barritas cereales','Galletas clásicas',
                  'Galletas de chocolate y rellenas','Wafer y barquillos',
                  'Surtido de pastas','Bollos chocolate, palmeras y donuts',
                  'Croissants, ensaimadas y napolitanas','Productos de campaña',
                  'Pan tostado, barritas y biscotes','Caramelos, chicles y golosinas',
                  'Caramelos y gominolas','Chicles','Repostería',',Para pastas',
                  'Cremas','En sobre','No refrigerado','Refrigerado',
                  'Purés','Lisas','Onduladas','Snacks','Snacks variados','Palomitas',
                  'Cortezas','Cocktail frutos secos','Especialidades','Otros encurtidos',
                  'Internacional','Sushi','Cocina arabe','Cocina mejicana',
                  'Cocina oriental','Listos para comer','Fritos selecta',
                  'Platos preparados y elaborados','Sandwiches y bocadillos',
                  'Ensaladas y ensaladillas','Gazpachos, cremas y untables',
                  'Pastas y arroces','Verduras','Carne','Pizzas refrigeradas',
                  'Tortillas','Fritos','Postres','Otros','Especialidades','Importación lata',
                  'Importación botella','Artesanas','Nacional botella','Nacional lata',
                  'Sin alcohol y de sabores','Sin alcohol (0,0 y 0,9)','Sabores',
                  'Cola','Naranja','Limón','Otros sabores','Bitter','Tónica','Té frío',
                 'Isotónicas y energéticas','Lata','Botella','Mosto','Zumos con leche',
                 'Zumos refrigerados','Zumos no refrigerados','Vinos','Aromatizado',
                 'Moscatel','Vinos dulces y generosos','Sangrías y combinados base vino',
                'Cava rosado','Licores y cremas','Vermuts y aperitivos','Lácteos y derivados',
                'Clásicas y chocolate','Integrales, digestivas y muesli','Pan, bollería y biscotes',
                'Chocolate y cacao','Mermeladas, miel y edulcorantes','Snacks, aperitivos y tortitas',
                'Bebidas y batidos vegetales','Infusiones y tés','Zumos y bebidas refrescantes',
                'Complementos nutricionales','Jaleas y polenta','Vitaminas y minerales',
                'Control de peso','Nutrición deportiva','Bio','Sin gluten',
                'Canelones, lasañas y pizzas','Croquetas, empanadas y rebozados','Salteados y revueltos',
                'Guisantes, judías y habas','Menestras y ensaladillas','Patatas',
                'Tarrinas','Cucuruchos y sandwiches','Bombones','Polos e infantiles',
                'Tartas , contesas y otros'
                ]

import json


def clean_items(data_list:list, keys_to_delete):

    """
    Deletes specified keys from each dictionary in a list of dictionaries.

    :param data_list: List of dictionaries containing product data.
    :param keys_to_delete: List of keys to remove from the dictionaries.
    :return: Modified list with keys removed.
    """
  # Create a new list that excludes any items where the first key is in keys_to_delete
    cleaned_list = [
        item for item in data_list if list(item.keys())[0] not in keys_to_delete
    ]
    
    return cleaned_list
  


def rename_keys_in_list(data_list: list, new_key: str, old_key: str) -> list:
    """
    Rename keys in all dictionaries in a list.
    
    :param data_list: List of dictionaries.
    :param new_key: The new name for the key.
    :param old_key: The old key name to replace.
    :return: The updated list with renamed keys.
    """
    for idx, jsn in enumerate(data_list):
        # Get the current top-level key (like "Secas")
        product_key = list(jsn.keys())[0]
        
        # If the top-level key matches old_key, rename it
        if product_key == old_key:
            # Create a new dictionary with the renamed key
            renamed_dict = {new_key: jsn[old_key]}
            data_list[idx] = renamed_dict  # Update the list in place

    return data_list


# File paths
input_file = 'raw_output_ids.json'
output_file = 'clean_output_ids.json'


# Read the JSON file
with open(input_file, 'r', encoding='utf-8') as file:
    data = json.load(file)
                    
clean_data = clean_items(data, DELETE_ITEMS)


# Rename 'old_key' to 'new_key'
# Could be an error if the key of the dictionary is Secas or Cocidas has another items and the sense change it.
# for example Secas: {puerros...}

renamed_data = rename_keys_in_list(clean_data,'Legumbres secas','Secas')
renamed_data = rename_keys_in_list(renamed_data,'Legumbres cocidas','Cocidas')
renamed_data =  rename_keys_in_list(renamed_data,'Aceitunas rellenas','Rellenas')
renamed_data = rename_keys_in_list(renamed_data,'Aceitunas rellenas','Rellenas')
renamed_data = rename_keys_in_list(renamed_data,'Aceitunas con hueso','Con hueso')
renamed_data = rename_keys_in_list(renamed_data,'Aceitunas sin hueso ','Sin hueso')
renamed_data = rename_keys_in_list(renamed_data,'Aceitunas negras','Negras')


clean_data =  renamed_data

with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(clean_data, file, indent=4, ensure_ascii=False)

print("The Json was succesfully cleaned!") 