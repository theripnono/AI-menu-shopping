# Alfa release: v.0.0.0
## TODO

Completar todas las tareas para el lanzamiento

### Server:
- [X] Añadir imagenes en los nodos
- [ ] Crear una funcion para insertar campos nuevos a los nodos.
- [ ] Crear una estimacion de la compra. Cuando GPT responde con las recetas poner total de la receta
- [ ] Loging: Función para añadir usuarios a la base de datos. Cuando el usuario se da de alta, se crea un nodo usuario.
- [X] Funcion purchase: Cuando el usuario compra, se crea un nodo relacionado con el usuario con el nodo de compra y este nodo esta relacionado con los nodos de productos.

### LLM:
- [ ] Crear un medidor tokenizador de manera que los prompts no sean muy largos. La gente hará frases cortas. 

### Test:
- [ ] Crear los Test de las funciones
- [X] Crear usuarios demo. Crear Jsons.
- [X] Crear nodos demo. Crear Jsons

### Neo4j Cypher:
- [X] Hay que rediseñar el nombre de los nodos, relaciones (verbos). Hay mezcla de ingles-castellano. Cambiar la relación "descripción"
- [ ] Crear queries para similitud entre usuarios.

- [X] Crear nodos de usuarios (mock-up)
- [X] Crear nodos de carritos de la compra (mock-up)

### Vue3:
- [ ] Refactor: Separar los componentes
- [X] Crear Boton comprar. Este botón genera el nodo Order.
- [ ] Crear un Dialog en lugar de "Alert" al comprar.
- [ ] En la pantalla de inicio sacar un carousel con los productos recomendados
- [X] Añadir el atributo "Sticky" al carrito de la compra
- [X] Cambiar el favicon
- [ ] Cuando hay una categoría mal y los productos no corresponden con el ingrediente, porque GPT me ha devuelto mal la categoría, habría que poner un botón donde:
	    1- Se abre un textarea y se pregunta al usuario qué está busacando, de manera que se inserta en la query y te busca.
      2-Vuelve  a buscar en la base de datos, con técnicas como lematización. De esta manera reduces el peligro de inyecciones maliciosas

# Forward steps:

Se da el caso que un usuario pide cosas muy específicas. Por ejemplo comida para niños pequeños, pero no quiere siempre tener que escribir en el prompt el texto. Se podría almacenar el texto, enlazarlo con el usuario y pasarlo como template.
