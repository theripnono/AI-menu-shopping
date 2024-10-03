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
import axios from 'axios';

export default {
  data() {
    return {
      message: '',
      userText: '',
      serverResponse: '',
      isLoading: false,
    };
  },
  mounted() {
    // Make a GET request to your Flask server
    axios.get('http://localhost:5000')
      .then(response => {
        
        this.message = response.data.message;
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  },
  methods: {
    submitText() {
      this.isLoading = true; // Iniciar el estado de carga
      this.serverResponse = ''; // Limpiar respuesta previa

      
      axios.post('http://localhost:5000/api/submit-text', { text: this.userText })
        .then(response => {
         
          this.serverResponse = response.data.message; // Corrected here
          this.isLoading = false;
        })
        .catch(error => {
          console.error('Error:', error);
          this.isLoading = false; 
        });
    }
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
