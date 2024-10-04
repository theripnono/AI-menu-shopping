<template>
  <div id="app">
    <h1>{{ message }}</h1>
    <div>
      <p>Asistente de compra de supermercado</p>
    </div>
    <div>
      <textarea v-model="userText" placeholder="Enter your text here" rows="4" cols="50"></textarea>
      <button @click="submitText">Generate Recipes</button>

      <div v-if="isLoading">
        <h2>Qué te parece si cocinamos...</h2>
        <div class="spinner"></div> 
      </div>

      <div v-else-if="serverResponse && serverResponse.length > 0">
      <div v-for="(recipe, index) in serverResponse" :key="index">
        <h2>{{ recipe.receta }}</h2>
        <div v-for="(ingrediente, ingKey) in recipe.ingredientes" :key="ingKey">
          <h3>{{ ingrediente.nombre }}</h3> <!-- Nombre del ingrediente -->
          <ul>    
            <li v-for="(producto, prodIndex) in ingrediente.productos" :key="prodIndex">
              {{ producto.product_name }} - {{ producto.product_brand }} 
              - {{ producto.price }}€
            </li> 
          </ul>
        </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import axios from 'axios';

export default {
  setup() {
    const message = ref('');
    const userText = ref('');
    const serverResponse = ref({});
    const isLoading = ref(false);

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
      serverResponse.value = null; // Clean previous response
      
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

    return { message, userText, serverResponse, isLoading, submitText };
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
