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
