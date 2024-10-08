<template>
    <v-container>
      <v-row>
        <!-- Sección para generar recetas -->

      <v-col cols="12">
          <div class="header" style="text-align: center;">
            <h1>BM</h1>
            <p>Supermercados</p>
          </div>
        <v-row>
          <v-col cols="8">
            <h1>{{ message }}</h1>
            <div>
              <h3><strong>Asistente de compra de Supermercado BM con IA</strong></h3>
            </div>
            <v-textarea 
              class="fixed-text" 
              variant="filled"
              auto-grow
              v-model="userText" 
              style="width: 500px"
              placeholder="Ejemplo: Quiero recetas de celiacos" 
            ></v-textarea>
            <v-btn style="margin-top: 20px;" @click="submitText">Generar Recetas</v-btn>

            <div v-if="isLoading" >
              <h2  style="background-color: rgb(254,237,36);">Qué te parece si cocinamos...</h2>
              <v-progress-circular color="primary" indeterminate></v-progress-circular>
            </div>

            <div v-else-if="serverResponse.length > 0" >
              <div v-for="(recipe, index) in serverResponse" :key="index">
                <div style="margin-top: 20px;">
                  <h2>¿Qué te parece {{ recipe.receta }}?</h2>
                  <v-btn @click="toggleIngredients(index)" style="margin: 20px;">
                    {{ showIngredients[index] ? 'Ocultar Ingredientes' : 'Mostrar Ingredientes' }}
                  </v-btn>
                </div>

                <v-row v-if="showIngredients[index]">
                  <v-col
                    v-for="(ingrediente, ingKey) in recipe.ingredientes"
                    :key="ingKey"
                    cols="6"
                  >
                    <v-card class="mb-2"  style="background-color: rgb(254,237,36);">
                      <v-card-title>{{ ingrediente.nombre }}</v-card-title>
                      <v-card-subtitle>Cantidad: {{ ingrediente.quantity }} {{ ingrediente.unit }}</v-card-subtitle>
                      <v-card-text>
                        <v-btn @click="toggleProducts(index, ingKey)" class="mb-2">
                          {{ showProducts[index] && showProducts[index][ingKey] ? 'Ocultar' : 'Mostrar' }} Productos
                        </v-btn>

                        <v-carousel
                          v-if="showProducts[index] && showProducts[index][ingKey]"
                          radius="5px"
                          height="200"
                          show-arrows="hover"                
                          hide-delimiter-background
                        >
                          <v-carousel-item v-for="(producto, prodIndex) in ingrediente.productos" :key="prodIndex">
                            <v-sheet height="100%" tile>
                              <v-row class="fill-height" align="center" justify="center">
                                <v-col cols="12" class="text-center">
                                  <h3>{{ producto.product_name }}</h3>
                                  <p>{{ producto.product_brand }}</p>
                                  <img :src="producto.img" :alt="producto.product_name" width="80" height="70">
                                  <p>{{ producto.price }}€</p>
                                  <v-btn @click="addCartProduct(producto)" color="primary">
                                    Add to Cart
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
          <h2>Productos del Carrito</h2>
          <v-list>
            <v-list-item-group >
              <v-list-item v-for="(item, index) in cartItems" :key="index">
                <v-list-item-content>
                  <v-list-item-title>{{ item.product.product_name }} (x{{ item.quantity }})</v-list-item-title>
                  <v-list-item-subtitle>{{ item.product.product_brand }}</v-list-item-subtitle>
                  <v-list-item-subtitle>Precio: {{ (item.product.price * item.quantity).toFixed(2) }}€</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-list-item-group>
          </v-list>
          <h3>Total: {{ cartTotal.toFixed(2) }}€</h3>
        </div>
          </v-col>
        </v-row>
        
      </v-col>
      </v-row>
    </v-container>
</template>

<script>
import { ref, onMounted } from 'vue';
import {  VBtn, VCarousel, VCard, VCardTitle, VCardText, VCarouselItem, VSheet, VRow, VCol, VList, VListItem } from 'vuetify/components';
import axios from 'axios';


export default {
  setup() {
    const message = ref('');
    const userText = ref('');
    const serverResponse = ref([]);
    const isLoading = ref(false);
    const cartItems = ref([]);
    const cartTotal = ref(0);

    // Estado para controlar la visibilidad de los productos
    const showProducts = ref({});
    // Estado para controlar la visibilidad de los ingredientes
    const showIngredients = ref({});

    onMounted(() => {
      axios.get('http://localhost:5000')
        .then(response => {
          message.value = response.data.message;
        })
        .catch(error => {
          console.error('Error fetching data:', error);
        });
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
      console.log('Producto añadido al carrito:', producto);
    };

    return { message, userText, serverResponse, isLoading,
            submitText, showProducts,cartTotal,
            toggleProducts, showIngredients,
            toggleIngredients, addCartProduct, cartItems };
  }
};
</script>

<style scoped>
textarea {
  width: 100%;
  margin-bottom: 10px;
  padding: 8px;
  resize: none;  /* Fixed height */

}

.cart-list{
justify-content: center;
position: sticky;
max-height: 400px;
top:0;
background-color: white;

}

.header {
  padding: 20px;
  text-align: center;
  background: #000000;
  color: rgb(254,237,36);
  font-size: 30px;
  font-weight: bold
}

.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-left-color: #000;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
