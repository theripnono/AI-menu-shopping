import { createRouter, createWebHistory } from 'vue-router';
import HelloWorld from '@/components/HelloWorld.vue'; // Ajusta la ruta según corresponda
import MyRecipes from '@/components/MyRecipes.vue';


const routes = [
    {
        path: '/',
        name: 'HelloWorld',
        component: HelloWorld,
    },
    {
        path: '/my-recipes',
        name: 'MyRecipes',
        component: MyRecipes,
    },
];

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes,
});

export default router;
