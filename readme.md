# Alfa release: v.0.0.0
## TODO

Completar todas las tareas para el lanzamiento

### Server:
- [X] Añadir imagenes en los nodos
- [ ] Crear una estimacion de la compra. Cuando GPT responde con las recetas poner total de la receta. Idea: Un objeto con todos los ingredientes, si hay ingredientes (o productos) repetidos eliminar. Este objeto hace el calc total del objeto.
- [X] Función para ordenar los productos con los ingredientes.
- [ ] Crear Loging: Función para añadir usuarios a la base de datos. Cuando el usuario se da de alta, se crea un nodo usuario.
- [X] Funcion purchase: Cuando el usuario compra, se crea un nodo relacionado con el usuario con el nodo de compra y este nodo esta relacionado con los nodos de productos.

### LLM:
- [ ] Crear un medidor tokenizador de manera que los prompts no sean muy largos. La gente hará frases cortas. 

### Test:
- [ ] Crear los Test de las funciones
- [X] Crear usuarios demo. Crear Jsons.
- [X] Crear carritos demo. 
- [X] Crear nodos demo. Crear Jsons

### Neo4j Cypher:
- [X] Hay que rediseñar el nombre de los nodos, relaciones (verbos). Hay mezcla de ingles-castellano. Cambiar la relación "descripción"
- [X] Crear queries para similitud entre usuarios.
- [X] Crear query: Cuando el usuario compra crear Nodo el Order y las relaciones con usuario y productos (u)->(o)->(p)
- [X] Crear nodos de usuarios (mock-up)
- [X] Crear nodos de carritos de la compra (mock-up)

### Vue3:
- [ ] Refactor: Separar los componentes
- [X] Crear Boton comprar. Este botón genera el nodo Order.
- [ ] Crear un Dialog en lugar de "Alert" al comprar.
- [X] En la pantalla de inicio sacar un carousel con los productos recomendados.
- [ ] Cambiar el spinner por menu.gif.
- [X] Añadir el atributo "Sticky" al carrito de la compra
- [X] Cambiar el favicon


# Forward steps:

- Se da el caso que un usuario pide cosas muy específicas. Por ejemplo comida para niños pequeños, pero no quiere siempre tener que escribir en el prompt el texto. Se podría almacenar el texto, enlazarlo con el usuario y pasarlo como template.
- Se podría sugerir las calorias de la receta.
- Escribir la receta. Crear un agente que basado en los ingredientes, haga la receta. guardarlo en el perfil del usuario.
Habría que pensar la manera que **no sea redundante**. Siempre que creas una receta, devuelve los ingredientes. Pero claro puede ser que por ejemplo siga teniendo aceite, leche, tomates en mi despensa.
- Crear nodos menu. Boton para guardar los menús asociarlos al usuario. La idea es que hacer menus con embeddings. 
- Ofrecer la posibilidad desde el la categoria poder buscar el producto.
