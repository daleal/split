import { createApp } from 'vue';
import { createPinia } from 'pinia';
import { router } from '@/router';
import App from '@/App.vue';

import '@/assets/styles/tailwind.css';

const pinia = createPinia();
const application = createApp(App);

application.use(pinia);
application.use(router);

application.mount('#app');
