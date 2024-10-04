<template>
  <v-app>
    <v-main>
      <h1>{{ message }}</h1>
      <div>
        <p>Asistente de compra de supermercado</p>
      </div>
      <div>
        <v-textarea clearable variant="solo"  v-model="userText" placeholder="Enter your text here" rows="4" cols="50"></v-textarea>
        <v-btn @click="submitText">Generate Recipes</v-btn>

        <div v-if="isLoading">
          <h2>Qué te parece si cocinamos...</h2>
          <v-progress-circular
            color="primary"
            indeterminate
          ></v-progress-circular>
        </div>

        <div v-else-if="serverResponse.length > 0">
          <div v-for="(recipe, index) in serverResponse" :key="index">
            <h2>{{ recipe.receta }}</h2>

            <div v-for="(ingrediente, ingKey) in recipe.ingredientes" :key="ingKey">
              <h3>{{ ingrediente.nombre }}</h3>

              <v-btn @click="toggleProducts(index, ingKey)">
                {{ showProducts[index] && showProducts[index][ingKey] ? 'Hide' : 'Show' }} Products
              </v-btn>

             <v-carousel v-if="showProducts[index] && showProducts[index][ingKey]" hide-delimiters show-arrows="hover">
            <v-carousel-item v-for="(producto, prodIndex) in ingrediente.productos" :key="prodIndex">
              <v-sheet height="100%" tile>
                <v-row class="fill-height" align="center" justify="center">
                  <v-col cols="12" class="text-center">
                    <h3>{{ producto.product_name }}</h3>
                    <p>{{ producto.product_brand }}</p>
                    <p>{{ producto.price }}€</p>
                  </v-col>
                </v-row>
              </v-sheet>
            </v-carousel-item>
          </v-carousel>
            </div>
          </div>
        </div>
      </div>
      </v-main>
    </v-app>
  </template>


<script>
import { ref, onMounted } from 'vue';
import { VApp, VMain, VBtn, VCarousel, VCarouselItem, VSheet, VRow, VCol } from 'vuetify/components'
import axios from 'axios';

export default {
  setup() {
    const message = ref('');
    const userText = ref('');
    const serverResponse = ref([]);
    const isLoading = ref(false);

    // Estado para controlar la visibilidad de los productos
    const showProducts = ref({});

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
          // Inicializar showProducts vacío para cada receta
          showProducts.value = {};
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

    return { message, userText, serverResponse, isLoading, submitText, showProducts, toggleProducts };
  }
};
</script>

<style scoped>
textarea {
  width: 100%;
  margin-bottom: 10px;
  padding: 8px;
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
