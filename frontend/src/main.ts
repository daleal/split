import { createApp } from 'vue';
import { createPinia } from 'pinia';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faCheck, faPlus, faXmark } from '@fortawesome/free-solid-svg-icons';
import { router } from '@/router';
import App from '@/App.vue';

import '@fortawesome/fontawesome-svg-core/styles.css';
import '@/assets/styles/tailwind.css';

library.add(faCheck, faPlus, faXmark);

const pinia = createPinia();
const application = createApp(App);

application.use(pinia);
application.use(router);

application.mount('#app');
