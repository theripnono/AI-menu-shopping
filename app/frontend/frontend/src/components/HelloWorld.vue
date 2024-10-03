<template>
  <div id="app">
    <h1>{{ message }}</h1>

    <div>
      <textarea v-model="userText" placeholder="Enter your text here" rows="4" cols="50"></textarea>
      <button @click="submitText">Generate Recipes</button>
      <div v-if="isLoading">
        <p>Loading...</p>
        <div class="spinner"></div> 
      </div>
      <div v-else>
        <p v-if="serverResponse">{{ serverResponse }}</p>
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
    const serverResponse = ref('');
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
      serverResponse.value = ''; // Limpiar respuesta previa

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
