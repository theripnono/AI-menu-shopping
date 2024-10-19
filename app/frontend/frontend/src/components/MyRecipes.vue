<template>
    <v-app>
      <!-- Menu -->
      <v-navigation-drawer expand-on-hover rail app>
        <v-list>
          <v-list-item
            prepend-avatar="https://cdn-icons-png.freepik.com/512/7244/7244486.png?uid=R159003661&ga=GA1.1.1763186972.1717243768"
            subtitle="dvdrg94@gmail.com"
            title="David Rosset"
          ></v-list-item>
        </v-list>
  
        <v-divider></v-divider>
  
        <v-list density="compact" nav>
          <v-list-item
            prepend-icon="mdi-silverware-clean"
            title="Generar Recetas"
            value="CreateRecipes"
            @click="$router.push({ name: 'HelloWorld' })"
          ></v-list-item>
          <v-list-item
            prepend-icon="mdi-book-open-page-variant"
            title="Mis recetas"
            value="misrecetas"
            @click="$router.push({ name: 'MyRecipes' })"
          ></v-list-item>
          <v-list-item prepend-icon="mdi-cog" title="Ajustes" value="config"></v-list-item>
        </v-list>
      </v-navigation-drawer>
  
      <div v-if="isLoading">
        <v-dialog v-model="isLoading" persistent max-width="400">
          <v-card class="d-flex flex-column align-center pa-4" style="height: 300px;">
            <div style="text-align: center">
              <h1>Cargando tu recetario</h1>
              <v-card-text>
                <img src="@/assets/gif/libro-de-cocina.gif" width="150" />
              </v-card-text>
            </div>
          </v-card>
        </v-dialog>
      </div>
  
      <v-container v-if="!isLoading"> <!-- Mostrar solo si no está cargando -->
        <v-row>
          <v-col
            v-for="(recipe, index) in myRecipes"
            :key="index"
            cols="12"
            md="4"
          >
            <v-card>
              <v-card-title>{{ recipe.menu_name }}</v-card-title>
              <v-card-actions>
                <v-btn @click="selectRecipe(recipe)">Seleccionar</v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-app>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  
  export default {
    setup() {
      const myRecipes = ref([]);
      const isLoading = ref(false);
  
      const fetchMyRecipes = async () => {
        isLoading.value = true; 
        
        try {
          const response = await axios.get('http://localhost:5000/api/my-recipes');
          myRecipes.value = response.data.message; // Asegúrate que la estructura de tu API coincida
        } catch (error) {
          console.error('Error fetching my recipes:', error);
        } finally {
            setTimeout(() => {
                isLoading.value = false; // Terminar loading
            }, 5000); 
          
        }
      };
  
      const selectRecipe = (recipe) => {
        console.log('Receta seleccionada:', recipe);
        // Aquí puedes añadir lógica para manejar la selección
      };
  
      onMounted(fetchMyRecipes);
  
      return {
        myRecipes,
        isLoading,
        selectRecipe,
      };
    },
  };
  </script>
  
  <style scoped>
  /* Estilos específicos del componente */
  </style>
  