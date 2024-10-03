<template>
  <div id="app">
    <h1>{{ message }} hola</h1>

    <div>
      <textarea v-model="userText" placeholder="Enter your text here" rows="4" cols="50"></textarea>
      <button @click="submitText">Generate Recipes</button>
      <p v-if="serverResponse">{{ serverResponse }}</p>
      <p v-else>Loading...</p>
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
    };
  },
  mounted() {
    // Make a GET request to your Flask server
    axios.get('http://localhost:5000')
      .then(response => {
        console.log(response.data.message)
        this.message = response.data.message;
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  },
  methods: {
    submitText() {
      axios.post('http://localhost:5000/api/submit-text', { text: this.userText })
        .then(response => {
          console.log(response.data.message)
          this.serverResponse = response.data.message; // Corrected here
        })
        .catch(error => {
          console.error('Error:', error);
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
</style>
