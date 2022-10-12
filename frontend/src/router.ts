import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import HomeView from '@/views/HomeView.vue';
import BillView from '@/views/bill/BillView.vue';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: HomeView,
  },
  {
    path: '/:billId',
    component: BillView,
  },
];

export const router = createRouter({
  history: createWebHistory(),
  routes,
});
