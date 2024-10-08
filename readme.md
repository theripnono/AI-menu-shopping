# TODO list
Proximos features:

Server:
- [X] Añadir imagenes en los nodos
- [ ] Crear una funcion para insertar campos nuevos a los nodos.
- [ ] Crear una estimacion de la compra. Cuando GPT responde con las recetas poner total de la receta
- [ ] Loging: Función para añadir usuarios a la base de datos. Cuando el usuario se da de alta, se crea un nodo usuario.

Test:
- [ ] Crear los Test de las funciones
- [ ] Crear usuarios demo. Crear Jsons.
- [ ] Crear nodos demo. Crear Jsons

Neo4j Cypher:
- [ ] Crear queries para similitud entre usuarios. Cosine similarity | Euclidean similarity
- [ ] Crear nodos de usuarios (mock-up)
- [ ] Crear nodos de carritos de la compra (mock-up)

Vue3:
- [ ] Refactor: Separar los componentes
- [ ] Añadir el atributo "Sticky" al carrito de la compra
- [X] Cambiar el favicon
- [ ] Cuando hay una categoría mal y los productos no corresponden con el ingrediente, porque GPT me ha devuelto mal la categoría, habría que poner un botón donde:
	    1- Se abre un textarea y se pregunta al usuario qué está busacando, de manera que se inserta en la query y te busca.
      2-Vuelve  a buscar en la base de datos, con técnicas como lematización. De esta manera reduces el peligro de inyecciones maliciosas

