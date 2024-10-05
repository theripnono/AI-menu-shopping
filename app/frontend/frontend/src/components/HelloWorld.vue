<template>
  <v-app class="full-width-app">
    <v-main class="full-width-app">
      <h1>{{ message }}</h1>
      <div>
        <p><strong>Asistente de compra de Supermercado BM con IA</strong></p>
      </div>
      
      <v-row>
        <!-- Sección para generar recetas -->
        <v-col cols="12" md="8">
          <v-textarea 
            class="fixed-text" 
            variant="solo" 
            v-model="userText" 
            placeholder="¿Qué te apetece que comamos esta semana?" 
          ></v-textarea>
          <v-btn style="margin-top: 20px;" @click="submitText">Generate Recipes</v-btn>

          <div v-if="isLoading">
            <h2>Qué te parece si cocinamos...</h2>
            <v-progress-circular color="primary" indeterminate></v-progress-circular>
          </div>

          <div v-else-if="serverResponse.length > 0">
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
                  <v-card class="mb-2">
                    <v-card-title>{{ ingrediente.nombre }}</v-card-title>
                    <v-card-subtitle>Cantidad: {{ ingrediente.quantity }} {{ ingrediente.unit }}</v-card-subtitle>
                    <v-card-text>
                      <v-btn @click="toggleProducts(index, ingKey)" class="mb-2">
                        {{ showProducts[index] && showProducts[index][ingKey] ? 'Ocultar' : 'Mostrar' }} Products
                      </v-btn>

                      <v-carousel
                        v-if="showProducts[index] && showProducts[index][ingKey]"
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
        <v-col cols="12" md="4">
          <h2>Productos del Carrito</h2>
          <v-list>
            <v-list-item-group>
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
        </v-col>
      </v-row>
    </v-main>
  </v-app>
</template>

<script>
import { ref, onMounted } from 'vue';
import { VApp, VMain, VBtn, VCarousel, VCard, VCardTitle, VCardText, VCarouselItem, VSheet, VRow, VCol, VList, VListItem } from 'vuetify/components';
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
        // If the product already exists, increase the quantity
        existingProduct.quantity += 1;
        } else {
        // If it's a new product, add it to the cart with quantity 1
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
}
.fixed-textarea {
  height: 100px; /* Fixed height */
  overflow-y: auto; /* Enables vertical scrolling */
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
