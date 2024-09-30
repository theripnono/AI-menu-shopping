import json
from dotenv import dotenv_values
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.output_parsers.json import SimpleJsonOutputParser

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
    
    return lcategories

def template_menu(categories_context:str)->dict:

    """
    Basic template for crete the menu

    :param deteil(str): user text input that is given as template details to
                        get more information. 
    """

    export = """
            [
                {{ 
                 "receta": "nombre de la receta", 
                 "ingredientes": [
                    {{
                        "categoria": "Nombre de la categoria",
                        "qty": Cantidad,
                        "unit": "Unidad de medida"
                    }},
                    {{
                        "categoria": "Nombre de la categoria",
                        "qty": Cantidad,
                        "unit": "Unidad de medida"
                    }}
                 ]
                }},
                etc..
            ]
        """
    
    # Here we use {context} as a variable that will be formatted later
    prompt_template = """
        Eres un asistente y tu trabajo consiste en crear recetas.
        Basándote en las categorías {context}, tienes que devolver únicamente
        las recetas y los ingredientes para elaborarlas.
        Ten en cuenta que el usuario puede pedir recetas vegetarianas o veganas.
        No devuelvas otra cosa que no sean ingredientes y recetas. 
        Importante: no inventes las categorías de los ingredientes.

        La respuesta tiene que llevar el siguiente formato en forma de lista de diccionarios:
        
        {export}
    """.format(context=categories_context, export=export)
    
    return prompt_template

def _generate_recipes(user_input:str) -> list:
    """
    Generate recipes based on given categories using GPT API via LangChain

    :param categories(str): A string of categories to base the recipes on
    :return: A list of dictionaries containing recipes and their ingredients
    """
    
    file  = 'preproces/clean_output_ids.json'
    context_categories = subcategories_as_context(file)

    print("Generating recepies...")

    # Initialize the language model
    config = dotenv_values(".env")
    apikey = config['OPENAI_API_KEY']
    llm = ChatOpenAI(temperature=0.7, openai_api_key=apikey)

    prompt_template = PromptTemplate.from_template(template_menu(context_categories))
    json_parser = SimpleJsonOutputParser()

    # Create the chain
    chain = (
        {"context": RunnablePassthrough()}
        | prompt_template
        | llm
        | StrOutputParser()
        | json_parser
    )

    # Generate the recipes
    response = chain.invoke(user_input)
    
    # Check if the response is empty or not valid JSON
    if len(response)==0:
        # Asumme that llm has not return any response
        print("Error: The response from the LLM is empty.")

        print("Generating response again, plaise wait...")
        tries=0
        while tries <= 5:
            response=_generate_recipes()
            if len(response)>0:
                break
            tries +=1
            if tries==5:
                print("Maximum number of attempts reached...")
    
    return response



