import './style.css'; // Import global CSS styles
import App from './App.vue'; // Import the main App component
import router from './router'; // Import the router configuration
import { createApp } from 'vue'; // Import createApp from Vue
import { createPinia } from 'pinia'; // Import createPinia for state management
import 'bootstrap-icons/font/bootstrap-icons.css'; // Import bootstrap icons

const initializeApp = () => {
  const app = createApp(App); // Create a new Vue application instance

  app.use(router); // Use the router instance in the app
  const pinia = createPinia(); // Create a new Pinia instance
  app.use(pinia); // Use Pinia for state management in the app

  app.mount('#app'); // Mount the Vue app to the DOM element with id 'app'
};

// Initialize and configure the app
initializeApp();
