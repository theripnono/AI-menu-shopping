<template>
  <div id="app">
    <h1>{{ message }}</h1>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      message: ''
    };
  },
  mounted() {
    // Make a GET request to your Flask server
    axios.get('http://localhost:5000/api/data')
      .then(response => {
        // Handle success - set data to response
        this.message = response.data.message;
      })
      .catch(error => {
        // Handle error
        console.error('Error fetching data:', error);
      });
  }
};
</script>
