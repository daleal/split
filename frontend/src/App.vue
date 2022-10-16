<script setup lang="ts">
import { useViewHeightHack } from '@/composables/viewHeightHack';
import PageFooter from '@/components/layout/PageFooter.vue';

useViewHeightHack();
</script>

<template>
  <div class="main-container w-full h-screen overflow-x-hidden flex flex-col justify-between">
    <div class="container max-w-md mx-auto mb-6 px-2 md:px-0">
      <router-view />
    </div>
    <PageFooter />
  </div>
</template>
