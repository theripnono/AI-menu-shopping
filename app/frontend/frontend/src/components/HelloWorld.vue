<template>
  <v-container>
    <v-row>
      <!-- Sección para generar recetas -->
      <v-col cols="12">
        <div class="header" style="text-align: center;">
          <h1 style="text-shadow: 1px 1px whitesmoke;"><strong>Asistente de compra inteligente</strong></h1>
        </div>
        <v-row>
          <v-col cols="12" md="8">
            <v-textarea class="fixed-text" variant="solo" auto-grow v-model="userText" 
              style="max-width: 100%; width: 500px" 
              placeholder="Ejemplo: Quiero recetas de celiacos">
            </v-textarea>
            <v-btn style="margin-top: 20px; margin-bottom: 20px" @click="submitText">
              {{ buttonText }}
            </v-btn>

            <!-- Productos Recomendados -->
            <v-row v-if="!hideRecommendedProducts && userText === '' && similarProducts.length !== 0 ">
              <div style="padding-top: 50px; padding-left: 10px;">
                <h2><strong>Productos recomendados para ti:</strong></h2>
              </div>
              <v-col cols="12">
                <v-carousel hide-delimiters show-arrows="hover" height="300" cycle interval="2000">
                  <v-carousel-item v-for="(product, index) in similarProducts" :key="index">
                    <v-card style="background-color: aliceblue; opacity: 0.7;">
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
              <v-dialog v-model="isLoading" persistent max-width="400">
                <v-card class="d-flex flex-column align-center pa-4" style="height: 420px;">
                  <div style="text-align: center">
                    <h1>¡Dejame pensar en algo súper bueno!</h1>
                    <v-card-text>
                      <img src="@/assets/gif/menu.gif" width="150" />
                    </v-card-text>
                    <h2>¡Espero que disfrutes cocinando!</h2>
                  </div>
                </v-card>
              </v-dialog>
            </div>

            <div v-else-if="serverResponse.length > 0">
              <v-expansion-panels multiple>
                <v-expansion-panel v-for="(recipe, index) in serverResponse" :key="index">
                  <v-expansion-panel-title>
                    <h2 style="text-shadow: 1px 1px whitesmoke;">¿Qué te parece: {{ recipe.receta }}?</h2>
                  </v-expansion-panel-title>

                  <v-expansion-panel-text>
                    <div style="position: relative; height: 80px;">
                      <!-- Botón de añadir receta a la cesta -->
                      <v-btn
                        @click="buyIngredients(index)"
                        size="large"
                        color="primary"
                        style="position: absolute; left: 0; top: 0; margin-bottom: 20px;">
                        Añadir receta a la cesta
                      </v-btn>

                      <!-- Botón de guardar receta -->
                      <v-btn v-if="!savedRecipes.includes(index)"
                        @click="saveRecipe(index)"
                        style="position: absolute; right: 0; top: 0; margin-bottom: 20px;"
                        prepend-icon="mdi-pencil-plus">
                         Guardar Receta
                      </v-btn>
                    </div>
                    <v-expansion-panels multiple>
                      <v-expansion-panel v-for="(ingrediente, ingKey) in recipe.ingredientes" :key="ingKey">
                        <v-expansion-panel-title>
                          {{ ingrediente.nombre }} - Cantidad: {{ ingrediente.quantity }} {{ ingrediente.unit }}
                        </v-expansion-panel-title>
                        <v-expansion-panel-text>
                          <v-carousel height="200" show-arrows="hover" hide-delimiters>
                            <v-carousel-item v-for="(producto, prodIndex) in ingrediente.productos" :key="prodIndex">
                              <v-sheet height="100%" tile>
                                <v-row class="fill-height" align="center" justify="center">
                                  <v-col cols="12" class="text-center">
                                    <h4>{{ producto.product_name }}</h4>
                                    <h4>{{ producto.product_brand }}</h4>
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
                        </v-expansion-panel-text>
                      </v-expansion-panel>
                    </v-expansion-panels>
                  </v-expansion-panel-text>
                </v-expansion-panel>
              </v-expansion-panels>
            </div>
          </v-col>

          <!-- Sección para mostrar el carrito -->
          <v-col cols="12" md="4">
            <v-expansion-panels>
              <v-expansion-panel>
                <v-expansion-panel-title>
                  <h2>Cesta ( {{ totalItemsInCart  }} artículos)</h2>
                </v-expansion-panel-title>

                <v-expansion-panel-text>
                  <div class="cart-list">
                    <v-list>
                      <v-list-item-group>
                        <v-list-item v-for="(item, index) in cartItems" :key="index">    
                          <v-list-item-content>
                            <v-list-item-title style="white-space: normal; word-wrap: break-word; padding: 5px;">
                              {{ item.product.product_name }} (x{{ item.quantity }})
                              <v-btn icon small @click="removeCartProduct(index)" style="width: 24px; height: 24px;">
                                <v-icon color="red" variant="tonal">mdi-minus</v-icon>
                              </v-btn>
                            </v-list-item-title>
                            <v-list-item-subtitle>{{ item.product.product_brand }}</v-list-item-subtitle>
                            <v-list-item-subtitle>Precio: {{ (item.product.price * item.quantity).toFixed(2) }}€</v-list-item-subtitle>
                          </v-list-item-content>
                        </v-list-item>
                      </v-list-item-group>
                    </v-list>
                    <hr>
                   
                  </div>
                
                </v-expansion-panel-text>
                <div style="text-align: center; padding-bottom: 20px;">
                  <v-btn  v-if="cartItems.length >= 1"  @click="purchaseOrder">
                       Comprar: {{ cartTotal.toFixed(2) }}€
                      <v-icon color="green">mdi-cart-check</v-icon>
                  </v-btn>
                </div>
              </v-expansion-panel>
            </v-expansion-panels>

          </v-col>

        </v-row>
      </v-col>

      <!--Succes Dialog-->
      <v-dialog v-model="showSuccessModal" max-width="400">
        <v-card>
          <v-card-title class="headline">¡Compra completada!</v-card-title>
          <v-card-text>
            Tu compra se ha realizado con éxito. ¡Gracias por tu compra!
            </v-card-text>
            <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" @click="showSuccessModal = false">Cerrar</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-row>
  </v-container>
</template>


<script>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';


export default {
  setup() {
    const similarProducts = ref([]);
    const userText = ref('');
    const serverResponse = ref([]);
    const isLoading = ref(false);
    const cartItems = ref([]);
    const cartTotal = ref(0);
    const showSuccessModal = ref(false); // Nuevo estado para el modal
    const savedRecipes = ref([]);

    const hideRecommendedProducts = ref(false)

    onMounted(() => {
      axios.get('http://localhost:5000')
        .then(response => {
          similarProducts.value = response.data.message;         
        })
        
        .catch(error => {
          console.error('Error fetching data:', error);
        });
        return similarProducts
    });

    const totalItemsInCart = computed(() => {
      return cartItems.value.reduce((total, item) => total + item.quantity, 0);
    });
    const submitText = () => {
      isLoading.value = true;
      serverResponse.value = []; // Limpiar la respuesta previa como lista vacía

      // inicializar el carrito
      cartItems.value = [];
      cartTotal.value = 0;
      savedRecipes.value = [];

      hideRecommendedProducts.value = true;

      axios.post('http://localhost:5000/api/submit-text', { text: userText.value })
        .then(response => {
          serverResponse.value = response.data.message;     
          isLoading.value = false;
         
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

    const saveRecipe = (index) => {
      if (!savedRecipes.value.includes(index)) {
        savedRecipes.value.push(index);
      }
      axios.post('http://localhost:5000/api/save-recipe', { recipe:serverResponse.value[index] })
      .then(response => {
      console.log('Receta guardada:', response.data);
      })
      .catch(error => {
      console.error('Error al guardar la receta:', error);
      });
    };

    const addCartProduct = (producto) => {
      const existingProduct = cartItems.value.find(item => item.product.product_name === producto.product_name);
      if (existingProduct) {
        // Si el producto existe añadir +1
        existingProduct.quantity += 1;
      } else {
        // Si no añadir nuevo item
        cartItems.value.push({ product: producto, quantity: 1 });
        console.log(producto)
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

    const purchaseOrder = () => {
      if (cartItems.value.length === 0) {
        console.log('No hay productos en el carrito.');
        return;
      }

      // Aquí puedes enviar los productos al servidor para completar la compra
      // Ejemplo de llamada POST al servidor:
      axios.post('http://localhost:5000/api/buy', { items: cartItems.value })
        .then(response => {
        showSuccessModal.value = true;
        // Limpiar el carrito después de la compra
       
        cartItems.value = [];
        cartTotal.value = 0;
        })
        .catch(error => {
          console.error('Error al procesar la compra:', error);
          alert('Ocurrió un error al intentar procesar la compra.');
        });

    };

    // Comprar todos los ingredientes->productos de la receta
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
      similarProducts, userText, serverResponse, isLoading,
      submitText, cartTotal, purchaseOrder,totalItemsInCart,
      buttonText,buyIngredients,showSuccessModal,hideRecommendedProducts,
      addCartProduct, cartItems, removeCartProduct,saveRecipe,savedRecipes
      
    };
  }
};
</script>

<style scoped>

/* https://colorhunt.co/palette/fff7d1ffecc8ffd09bffb0b0 */
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

</style>
