<template>
  <v-container>
    <v-row>
      <!-- Sección para generar recetas -->

      <v-col cols="12">
        <div class="header" style="text-align: center; ">
          <h1 style=" text-shadow: 1px 1px whitesmoke;"><strong>Asistente de compra inteligente</strong>
          </h1>
        </div>
        <v-row>
          <v-col cols="8">

            <!-- metodo get -->
            <!-- <h1>{{ message }}</h1> -->
            <div>

            </div>

            <v-textarea class="fixed-text" variant="solo" auto-grow v-model="userText" style="width: 500px"
              placeholder="Ejemplo: Quiero recetas de celiacos"></v-textarea>
            <v-btn style="margin-top: 20px;" @click="submitText">
              {{ buttonText }}
            </v-btn>

            <v-row>
              <div style="padding-top: 50px; padding-left: 10px;">
                <h2 style="background-color: aliceblue;"><strong>Productos Recomendados para ti:</strong></h2>
              </div>
              <v-col cols="12"> 
              <v-carousel hide-delimiters show-arrows="hover" height="300" cycle interval="2000" >

                <v-carousel-item v-for="(product, index) in similar_products" :key="index">
                  <v-card style="background-color: aliceblue;opacity: 0.7;">
                    <v-img :src="product.img" height="200px"></v-img>
                    <v-card-title>{{ product.product_name }}</v-card-title>
                    <v-card-subtitle>
                      <span v-if="product.product_brand">{{ product.product_brand }}</span>
                      <span v-else>Marca desconocida</span>
                    </v-card-subtitle>
                    <v-card-text>
                      <p>Precio: €{{ product.price.toFixed(2) }}</p>
                    </v-card-text>
                  </v-card>
                </v-carousel-item>
              </v-carousel>
            </v-col>
            </v-row>
          
            <div v-if="isLoading">
              <h2>Voy a pensar que en algo rico...</h2>
              <v-progress-circular color="blue-lighten-3"
               model-value="20"
                indeterminate
                :size="84"
                :width="12"
                ></v-progress-circular>
            </div>

            <div v-else-if="serverResponse.length > 0">
              <div v-for="(recipe, index) in serverResponse" :key="index">
                <div style="margin-top: 20px; background-color: aliceblue" >
                  <h2 style="text-shadow: 1px 1px whitesmoke;">¿Qué te parece: {{ recipe.receta }}?</h2>
                  <v-btn @click="toggleIngredients(index)" style="margin: 20px;">
                    {{ showIngredients[index] ? 'Ocultar Ingredientes' : 'Mostrar Ingredientes' }}
                  </v-btn>
                  <v-btn @click="buyIngredients(index)" color="primary">
                    Comprar ingredientes
                  </v-btn>
                </div>

                <v-row v-if="showIngredients[index]">
                  <v-col v-for="(ingrediente, ingKey) in recipe.ingredientes" :key="ingKey" cols="6">

                    <v-card class="mb-2" style="background-color:aliceblue ;">
                      <v-card-title>{{ ingrediente.nombre }}</v-card-title>
                      <v-card-subtitle>Cantidad: {{ ingrediente.quantity }} {{ ingrediente.unit }}</v-card-subtitle>
                      <v-card-text>

                        <v-btn @click="toggleProducts(index, ingKey)" class="mb-2">
                          {{ showProducts[index] && showProducts[index][ingKey] ? 'Ocultar' : 'Mostrar' }} Productos
                        </v-btn>

                        <v-carousel v-if="showProducts[index] && showProducts[index][ingKey]" height="200"
                          show-arrows="hover" hide-delimiters>

                          <v-carousel-item v-for="(producto, prodIndex) in ingrediente.productos" :key="prodIndex">
                            <v-sheet height="100%" tile>
                              <v-row class="fill-height" align="center" justify="center">
                                <v-col cols="12" class="text-center">
                                  <h3>{{ producto.product_name }}</h3>
                                  <p>{{ producto.product_brand }}</p>
                                  <img :src="producto.img" :alt="producto.product_name" width="80" height="70">
                                  <p>{{ producto.price }}€</p>
                                  <v-btn @click="addCartProduct(producto)" color="primary">
                                    Añadir
                                  </v-btn>
                                </v-col>
                              </v-row>
                            </v-sheet>
                          </v-carousel-item>
                        </v-carousel>
                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-row>
              </div>
            </div>
          </v-col>

          <!-- Sección para mostrar el carrito en la derecha -->
          <v-col cols="4">
            <div class="cart-list">
              <h2>Cesta</h2>
              <v-list>
                <v-list-item-group>
                  <v-list-item v-for="(item, index) in cartItems" :key="index">
                    <v-list-item-content>
                      <v-list-item-title style="white-space: normal; word-wrap: break-word; padding: 5px;
                      ">{{
                        item.product.product_name }}
                        (x{{ item.quantity }})
                        <v-btn icon small @click="removeCartProduct(index)" style="width: 24px; height: 24px;">
                          <v-icon color="red" variant="tonal">mdi-minus</v-icon>
                        </v-btn>
                      </v-list-item-title>

                      <v-list-item-subtitle>{{ item.product.product_brand }}</v-list-item-subtitle>



                      <v-list-item-subtitle>Precio: {{ (item.product.price * item.quantity).toFixed(2)
                        }}€</v-list-item-subtitle>


                    </v-list-item-content>
                  </v-list-item>
                </v-list-item-group>
              </v-list>
              <hr>
              <h3>Total: {{ cartTotal.toFixed(2) }}€</h3>´
              <v-btn 
                v-if="cartItems.length >= 1" append-icon="" @click="buyItems">
                Comprar
                <v-icon color="green">mdi-cart-check</v-icon>             
              </v-btn>
            </div>

          </v-col>
        </v-row>

      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import { VBtn, VCarousel, VCard, VCardTitle, VCardText, VCarouselItem, VSheet, VRow, VCol, VList, VListItem } from 'vuetify/components';
import axios from 'axios';


export default {
  setup() {
    const similar_products = ref([]);
    const userText = ref('');
    const serverResponse = ref([]);
    const isLoading = ref(false);
    const cartItems = ref([]);
    const cartTotal = ref(0);
    // Mostrar productos recomendados por defecto


    // Estado para controlar la visibilidad de los productos
    const showProducts = ref({});
    // Estado para controlar la visibilidad de los ingredientes
    const showIngredients = ref({});

    onMounted(() => {
      axios.get('http://localhost:5000')
        .then(response => {
          similar_products.value = response.data.message;
         //hacer una lista aleatoria de productos
         
        })
        
        .catch(error => {
          console.error('Error fetching data:', error);
        });
        return similar_products
    });

    const submitText = () => {
      isLoading.value = true;
      serverResponse.value = []; // Limpiar la respuesta previa como lista vacía

      // inicializar el carrito
      cartItems.value = [];
      cartTotal.value = 0;
        

      
  
      axios.post('http://localhost:5000/api/submit-text', { text: userText.value })
        .then(response => {
          serverResponse.value = response.data.message;
         
          isLoading.value = false;
          // Inicializar showProducts y showIngredients vacíos para cada receta
          showProducts.value = {};
          showIngredients.value = {};
        })
        .catch(error => {
          console.error('Error:', error);
          isLoading.value = false;
        });
    };

    // Propiedad computada para cambiar el texto del botón
    const buttonText = computed(() => {
      return userText.value ? 'Generar Recetas' : 'Recetas Aleatorias';
    });

    // Función para alternar la visibilidad de los productos
    const toggleProducts = (recipeIndex, ingKey) => {
      if (!showProducts.value[recipeIndex]) {
        showProducts.value[recipeIndex] = {};
      }
      showProducts.value[recipeIndex][ingKey] = !showProducts.value[recipeIndex][ingKey];
    };

    // Función para alternar la visibilidad de los ingredientes
    const toggleIngredients = (recipeIndex) => {
      showIngredients.value[recipeIndex] = !showIngredients.value[recipeIndex];
    };

    const addCartProduct = (producto) => {
      const existingProduct = cartItems.value.find(item => item.product.product_name === producto.product_name);
      if (existingProduct) {
        // Si el producto existe añadir +1
        existingProduct.quantity += 1;
      } else {
        // Si no añadir nuevo item
        cartItems.value.push({ product: producto, quantity: 1 });
      }

      cartTotal.value = Math.round((cartTotal.value + producto.price + Number.EPSILON) * 100) / 100
     
    };

    const removeCartProduct = (index) => {
      const item = cartItems.value[index];

      if (item.quantity > 1) {
        // Restar una unidad
        item.quantity -= 1;
        cartTotal.value = Math.round((cartTotal.value - item.product.price + Number.EPSILON) * 100) / 100;
      } else {
        // Eliminar el producto si solo queda uno
        cartTotal.value = Math.round((cartTotal.value - item.product.price + Number.EPSILON) * 100) / 100;
        cartItems.value.splice(index, 1); // Elimina el producto del carrito
      }
    };

    const buyItems = () => {
      if (cartItems.value.length === 0) {
        console.log('No hay productos en el carrito.');
        return;
      }

      // Aquí puedes enviar los productos al servidor para completar la compra
      // Ejemplo de llamada POST al servidor:
      axios.post('http://localhost:5000/api/buy', { items: cartItems.value })
        .then(response => {

          // Muestra un mensaje de éxito si la compra fue exitosa
          alert('¡Compra completada con éxito!');
          // Limpiar el carrito después de la compra
          cartItems.value = [];
          cartTotal.value = 0;
        })
        .catch(error => {
          console.error('Error al procesar la compra:', error);
          alert('Ocurrió un error al intentar procesar la compra.');
        });

    };

    const buyIngredients = (recipeIndex) => {
    const recipe = serverResponse.value[recipeIndex]; // Toma la receta específica seleccionada
    for (let key in recipe.ingredientes) {
        const producto = recipe.ingredientes[key].productos[0];
        if (producto) {
            addCartProduct(producto);
        }
      }
  };


    return {
      similar_products, userText, serverResponse, isLoading,
      submitText, showProducts, cartTotal, buyItems,
      toggleProducts, showIngredients, buttonText,buyIngredients,
      toggleIngredients, addCartProduct, cartItems, removeCartProduct
    };
  }
};
</script>

<style scoped>
textarea {
  width: 100%;
  margin-bottom: 10px;
  padding: 8px;
  resize: none;
  /* Fixed height */

}

.cart-list {
  justify-content: center;
  position: sticky;
  max-height: 400px;
  top: 0;
  overflow-y: auto; /* Habilita el scroll vertical */
  padding: 10px;
  background-color: #f9f9f9; /* Color de fondo para darle contraste */
  border-radius: 8px; /* Bordes redondeados */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Sombra sutil */
}

/* Estilos para la barra de scroll en navegadores Webkit (Chrome, Edge, Safari) */
.cart-list::-webkit-scrollbar {
  width: 8px; /* Ancho de la barra de scroll */
}

.cart-list::-webkit-scrollbar-track {
  background: #e0e0e0; /* Color del track (fondo de la barra de scroll) */
  border-radius: 8px;
}


.header {
  padding: 20px;
  /* background: #000000;
  background-image: url("https://img.freepik.com/foto-gratis/vista-superior-monton-composicion-verduras-frescas_23-2148642957.jpg?t=st=1728413016~exp=1728416616~hmac=f9841c5980dd87efae8cc802c2eddc1105ade6e819b887edc210c0d325e07e1d&w=996");
  height: 100px; */

}


.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-left-color: #000;
  border-radius: 50%;
  width: 50px;
  height: 5px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}
</style>
