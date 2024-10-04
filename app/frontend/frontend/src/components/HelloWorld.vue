<template>
  <v-app>
    <v-main>
      <h1>{{ message }}</h1>
      <div>
        <p><strong>Asistente de compra de supermercado BM con IA</strong></p>
      </div>
      <div>
        <v-textarea class="fixed-text" variant="solo" v-model="userText" placeholder="¿Qué te apetece que comamos esta semana?" ></v-textarea>
        <v-btn style="margin-top: 20px;" @click="submitText">Generate Recipes</v-btn>

        <div v-if="isLoading">
          <h2>Qué te parece si cocinamos...</h2>
          <v-progress-circular color="primary" indeterminate></v-progress-circular>
        </div>

        <div v-else-if="serverResponse.length > 0">
          <div v-for="(recipe, index) in serverResponse" :key="index">
            <div style="margin-top: 20px;">
              <h2>¿Qué te parece una {{ recipe.receta }}?</h2>
              <v-btn @click="toggleIngredients(index)" style="margin-top: 20px;">
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
                              <v-btn @click="handleProductClick(producto)" color="primary">
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
      </div>
    </v-main>
  </v-app>
</template>

<script>
import { ref, onMounted } from 'vue';
import { VApp, VMain, VBtn, VCarousel, VCard, VCardTitle, VCardText, VCarouselItem, VSheet, VRow, VCol } from 'vuetify/components';
import axios from 'axios';

export default {
  setup() {
    const message = ref('');
    const userText = ref('');
    const serverResponse = ref([]);
    const isLoading = ref(false);

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

    return { message, userText, serverResponse, isLoading, submitText, showProducts, toggleProducts, showIngredients, toggleIngredients };
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
