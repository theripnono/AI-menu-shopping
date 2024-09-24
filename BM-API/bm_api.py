import json, os, requests, shutil, datetime
from tqdm import tqdm
"""
Puedo sacar los productos de las subcategorias pasando el ID
https://www.online.bmsupermercados.es/api/rest/V1.0/catalog/product?&orderById=7&categories={id}
"""
class BMAPI:
    """
    Get all data from BM Basque Supermarket.
    """
    def __init__(self):
        self._categories=self._get_all_ids()

    """
    Basic methods to get data from BM supermarket
    """

    def _export_to_json(self, data:list[dict], file_name:str=None)->str:
        """
        Converts a list of dictionaries into a JSON-formatted string.
        
        Parameters:
        data (list of dict): The list of dictionaries to be converted.
        
        Returns:
        str: A JSON-formatted string.
        """
        if file_name==None:
            file_name="output"
        try:
            # Convert the list of dictionaries to a JSON string
            with open(f'{file_name}.json', 'w') as file:
                json.dump(data, file, indent=4)
            print('Succesfuly exported to JSON!')
        
        except TypeError as e:
            print(f"Error converting to JSON: {e}")
            return None
        
    def _get_all_ids(self)->list[dict]:
        
        """
        Main function that gets all ids of categories and subcategories
        return: list all categories and subcategories.
        
        """
        url = "https://www.online.bmsupermercados.es/api/rest/V1.0/shopping/category/menu"
        response = requests.get(url)
        
        all_items = []

        if response.status_code == 200:
            data = response.json()

            for category in data:
                r ={}
                category_id= category['id']
                category_name= category['nombre']

                r['category_name']=category_name
                r['id']=category_id
                r['subcategories']=[]
                
                subcategories1 = category['subcategories']
                
                if len(subcategories1)>0:
                    
                    # BM has many levels of products segmentation. 
                    #
                    # Actually 11 levels are created
                    for subcategories in subcategories1:

                        subcategory_id=subcategories['id']
                        subcategory_name = subcategories['name']

                        r['subcategories'].append({'subcategory_id':subcategory_id,'subcategory_name':subcategory_name})

                        subcategories2 = subcategories['subcategories']
                        
                        if len(subcategories2)>0:
                            
                            for subcategories in subcategories2:
                                subcategory_id=subcategories['id']
                                subcategory_name = subcategories['name']

                                r['subcategories'].append({'subcategory_id':subcategory_id,'subcategory_name':subcategory_name})
                                
                                subcategories3 = subcategories['subcategories']

                                if len(subcategories3)>0:
                                
                                    
                                    for subcategories in subcategories3:
                                        subcategory_id=subcategories['id']
                                        subcategory_name = subcategories['name']

                                        r['subcategories'].append({'subcategory_id':subcategory_id,'subcategory_name':subcategory_name})

                                        subcategories4 = subcategories['subcategories']

                                        if len(subcategories4)>0:

                                            for subcategories in subcategories4:
                                                subcategory_id=subcategories['id']
                                                subcategory_name = subcategories['name']

                                                r['subcategories'].append({'subcategory_id':subcategory_id,'subcategory_name':subcategory_name})

                                                subcategories5 = subcategories['subcategories']

                                                if len(subcategories5)>0:

                                                    for subcategories in subcategories5:
                                                        subcategory_id=subcategories['id']
                                                        subcategory_name = subcategories['name']

                                                        r['subcategories'].append({'subcategory_id':subcategory_id,'subcategory_name':subcategory_name})

                                                        subcategories6 = subcategories['subcategories']

                                                        if len(subcategories6)>0:

                                                            for subcategories in subcategories6:
                                                                subcategory_id=subcategories['id']
                                                                subcategory_name = subcategories['name']

                                                                r['subcategories'].append({'subcategory_id':subcategory_id,'subcategory_name':subcategory_name})

                                                                subcategories7 = subcategories['subcategories']


                                                            if len(subcategories7)>0:

                                                                for subcategories in subcategories7:
                                                                    subcategory_id=subcategories['id']
                                                                    subcategory_name = subcategories['name']

                                                                    r['subcategories'].append({'subcategory_id':subcategory_id,'subcategory_name':subcategory_name})

                                                                    subcategories8 = subcategories['subcategories']
                                                                    
                                                                    if len(subcategories8)>0:

                                                                        for subcategories in subcategories8:
                                                                            subcategory_id=subcategories['id']
                                                                            subcategory_name = subcategories['name']

                                                                            r['subcategories'].append({'subcategory_id':subcategory_id,'subcategory_name':subcategory_name})

                                                                            subcategories9 = subcategories['subcategories']
                                                                        
                                                                        if len(subcategories9)>0:

                                                                            for subcategories in subcategories9:
                                                                                subcategory_id=subcategories['id']
                                                                                subcategory_name = subcategories['name']

                                                                                r['subcategories'].append({'subcategory_id':subcategory_id,'subcategory_name':subcategory_name})

                                                                                subcategories10 = subcategories['subcategories']
                                                                            
                                                                            if len(subcategories10)>0:

                                                                                for subcategories in subcategories10:
                                                                                    subcategory_id=subcategories['id']
                                                                                    subcategory_name = subcategories['name']

                                                                                    r['subcategories'].append({'subcategory_id':subcategory_id,'subcategory_name':subcategory_name})

                                                                                    subcategories11 = subcategories['subcategories']
                                                                                    if len(subcategories11)>0:
                                                                                        subcategory_id=subcategories11['id']
                                                                                        subcategory_name = subcategories11['name']

                                                                                        r['subcategories'].append({'subcategory_id':subcategory_id,'subcategory_name':subcategory_name})

                else:
                    print(f'the category {category_name} has not subcategories')
                
                all_items.append(r)
        return all_items
    
    def show_categories(self, details=False):
        """
        Get all categories from BM

        :param details: if subcategories = True it shows all the subcatecories
        """
        print(f"These are the main categories ->")

        if not details:
            for category in self._categories:
                    print(f"- ID: {category['id']} {category['category_name']}")
                 
        else:
            categories = self._categories
            for category in categories:
                print("____________________________________________________________")
                print(f"Category: {category['category_name']} || id: {category['id']} has these subcategories: ")
                print("__________________________________________________________")
                subcatregories = category['subcategories']
                for subcategory in subcatregories:    
                    print(f"{subcategory['subcategory_name']} || id: {subcategory['subcategory_id']}")
  
    def show_discounts(self):
        """
        Show the categories and subcategories discounts to help.

        The purpose of this method is to catch discounts every day creating
        a cron and launching every day the job.

        :param save_data: if True -> store the data in a variable
        return: list of tuples with ids and subcategories names
        """
        discounts_categories = [x for x in self.categories if x['category_name']=='Ofertas'][0]['subcategories']
        print("These are the discounts subcategories: ")

        for discounts in discounts_categories:
            print(f"{discounts['subcategory_id']} || {discounts['subcategory_name']}")  
            
    def get_discounts(self, food:bool=True)->list[dict]:

        """
        Get all the discounts of the day if food param is false get all the discounted items. 

        The purpose of this method is to catch discounts every day creating
        a cron and launching every day the job.

        NOTE: Keep in mind that the method makes a lot of GET's to the server, so the server could block your
              your IP.
        :param food bool: Only get the foods items from the server.
        return: list of discounts items
        """

        def _get_food_discounts()->list[dict]:
            """
            Get only food categories instead all cagories
            """
            offers_list=[]
            discounts_categories = [x for x in self.categories if x['category_name']=='Ofertas'][0]['subcategories']

            for category in tqdm(discounts_categories, desc='Getting categories...', leave=True):
                subs = category['subcategories']
                name = category['category_name']

                for subcategory in tqdm(subs, desc=f'Getting subcategories from {name}...', leave=False):

                    id = subcategory['subcategory_id']
                    url_offers=f"https://www.online.bmsupermercados.es/api/rest/V1.0/catalog/product?&orderById=7&categories={id}"

                    response = requests.get(url_offers)
                    if response.status_code == 200:
                        data = response.json()

                        if data['totalCount']>0:
                            products = data['products']
                            
                            for product in products:

                                r ={}

                                product_id = product['id']
                                product_ean =  product['ean']
                                product_name = product['productData']['name']
                                product_seo = product['productData']['seo']

                                r['product_data'] = (product_id,product_ean,product_seo,product_name)

                                offers_list.append(r)
            return offers_list
        
        offers_list=[]
        discounts_categories = [x for x in self.categories if x['category_name']=='Ofertas'][0]['subcategories']

        print("Downloading data... this could take several minuts...")
        print("You can use get_discounts_by_category(category) for faster results")

        if food:
            print("All food discounts items are downloaded")  
            return _get_food_discounts()
        
        else:    
            for category in discounts_categories:
                subs = category['subcategories']
                for subcategory in subs:
                    id = subcategory['subcategory_id']
                    url_offers=f"https://www.online.bmsupermercados.es/api/rest/V1.0/catalog/product?&orderById=7&categories={id}"

                    response = requests.get(url_offers)
                    if response.status_code == 200:
                        data = response.json()

                        products = data['products']
                        
                        for product in products:

                            r ={}

                            product_id = product['id']
                            product_ean =  product['ean']
                            product_name = product['productData']['name']
                            product_seo = product['productData']['seo']

                            r['product_data'] = (product_id, product_ean, product_seo, product_name)

                            offers_list.append(r)
            print("All discount items are downloaded")   
            return offers_list

    def get_products_by_category(self, category_name:str, export=True)->list[dict]:
        """
        Get the items filtered by category
        e.g:
           items =  get_items_by_category('Bebidas')
        ------------------------------------------------------------------------   
        These are the avaible categories for this method
        - Ofertas
        - Frescos
        - Alimentación
        - Bebidas
        - Eco-saludable
        - Congelados
        - Cuidado del hogar
        - Bebé
        - Cuidado personal
        - Mascotas
        :param category: string of the category
        return: list[dict]
        """
        products_list=[]


        # Filtered by category
        categories = [x for x in self._categories if x['category_name']==category_name][0]['subcategories']

        for subcategory in tqdm(categories, desc=f'Downloading {category_name} data...: '):

            id = subcategory['subcategory_id']
            url_offers=f"https://www.online.bmsupermercados.es/api/rest/V1.0/catalog/product?&orderById=7&categories={id}"

            response = requests.get(url_offers)
            if response.status_code == 200:
                data = response.json()

                if data['totalCount']>0:
                    products = data['products']
                    
                    for product in products:

                        r ={}

                        product_id = product['id']
                        product_ean =  product['ean']
                        product_name = product['productData']['name']
                        product_seo = product['productData']['seo']

                        r['product_data'] = {'product_id':product_id,
                        'product_ean':product_ean, 'product_seo': product_seo, 'product_name':product_name}

                        products_list.append(r)

        print("All data downloaded successfully!")

        if export:
            self._export_to_json(products_list, category_name)
        return products_list
    
    def get_products_by_id(self, id:int, export=True)->list[dict]:

        """
        Get all items from one id
        :param id: Id of the category/subcategory
        :export: If True export into JSON file
        return: list of dictionaries containing subcategories info
        """

        url=f"https://www.online.bmsupermercados.es/api/rest/V1.0/catalog/product?&orderById=7&categories={id}"
        response = requests.get(url)
            
        products_list=[] 

        if response.status_code == 200:
            data = response.json()

            if data['totalCount']>0:
                products = data['products']
                name=products[0]['categories'][0]['name'].lower().strip()
                for product in tqdm(products, desc=f'Downloading products: {name}...: ', leave=True):
                        r ={}

                        product_id = product['id']
                        product_ean =  product['ean']
                        product_name = product['productData']['name']
                        product_seo = product['productData']['seo']

                        r['product_data'] = {'product_id':product_id,
                                            'product_ean':product_ean,
                                            'product_seo': product_seo,
                                            'product_name':product_name}

                        products_list.append(r)

                print("All data downloaded successfully!")

            if export:    
                self._export_to_json(products_list, name)

            return products_list

    def get_products_by_ids(self, ids:list[int], export=True)->list[dict]:

        """
        Get all items from multiple ids
        :param ids: list with ids
        :param export: export the output into JSON file
        :export: If True export into JSON file
        return: list of dictionaries containing subcategories info
        """
        products_list=[] 

        for id in ids:
            url=f"https://www.online.bmsupermercados.es/api/rest/V1.0/catalog/product?&orderById=7&categories={id}"
            response = requests.get(url)
                
    
            if response.status_code == 200:
                data = response.json()

                if data['totalCount']>0:
                    products = data['products']
                    name=products[0]['categories'][0]['name'].lower().strip()
                    for product in tqdm(products, desc=f'Downloading products: {name}...: ', leave=True):
                            r ={}

                            product_id = product['id']
                            product_ean =  product['ean']
                            product_name = product['productData']['name']
                            product_seo = product['productData']['seo']

                            r['product_data'] = {'product_id':product_id,
                                                'product_ean':product_ean,
                                                'product_seo': product_seo,
                                                'product_name':product_name}

                            products_list.append(r)

                    print("All data downloaded successfully!")
        if export:     
            self._export_to_json(products_list, 'output_ids')

        return products_list

bm = BMAPI()
categories = bm._categories
print(bm.show_all_data())
#bm.show_all_data()
bm.get_products_by_ids([1245,1472])

#productos = bm.get_products_by_category('Frescos')

