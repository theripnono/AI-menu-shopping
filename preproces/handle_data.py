import json
import items_to_delete

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
input_file = 'preproces/output_img_ids.json'
output_file = 'preproces/products.json'

# Read the JSON file
with open(input_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

items_to_delete=items_to_delete.DELETE_ITEMS
clean_data = clean_items(data, items_to_delete)


# Rename 'old_key' to 'new_key'
# Could be an error if the key of the dictionary is Secas or Cocidas has another items and the sense change it.
# for example Secas: {puerros...}

renamed_data = rename_keys_in_list(clean_data,'Legumbres secas','Secas')
renamed_data = rename_keys_in_list(renamed_data,'Legumbres cocidas','Cocidas')
renamed_data = rename_keys_in_list(renamed_data,'Aceitunas rellenas','Rellenas')
renamed_data = rename_keys_in_list(renamed_data,'Aceitunas rellenas','Rellenas')
renamed_data = rename_keys_in_list(renamed_data,'Aceitunas con hueso','Con hueso')
renamed_data = rename_keys_in_list(renamed_data,'Aceitunas sin hueso ','Sin hueso')
renamed_data = rename_keys_in_list(renamed_data,'Aceitunas negras','Negras')

clean_data =  renamed_data

with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(clean_data, file, indent=4, ensure_ascii=False)

print("The Json was succesfully cleaned!") 