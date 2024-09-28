import json
from dotenv import dotenv_values
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings


config = dotenv_values(".env")
apikey = config['OPENAI_API_KEY']
llm = ChatOpenAI(temperature=0.7, openai_api_key=apikey)

# high temperature for better imagination 

"""
The idea is to give the LLM a context based on categories. These categories,
is passed as a parameter to the neo4j graph. 

The response from the llm must have the following result:

Recipe:
Ingredidient -> Category
Ingredient -> Category

Ouput structure:

    [
        {
        ingredient:str(category),
        qty: int(quantity),
        unit: unit
        },
        {
        ingredient:str(category),
        qty: int(quantity),
        unit: unit
        },
    ]

"""


def subcategories_as_context(input_file:str)->list[str]:
    
    """
    Get all keys of cleaned json in order to use as llm context.
    
    """
    lcategories =[]
    # Read the JSON file
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    for item in data: 
        lcategories.append(list(item.keys())[0])
    lcategories = list( dict.fromkeys(lcategories))
    print(lcategories)
    
    return lcategories

file  = 'clean_output_ids.json'
context_categories = subcategories_as_context(file)

print(context_categories)