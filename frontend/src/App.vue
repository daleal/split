<script setup lang="ts">
import PageFooter from '@/components/layout/PageFooter.vue';
</script>

<template>
  <div class="w-screen h-screen overflow-x-hidden flex flex-col justify-between">
    <div class="container max-w-md mx-auto pb-6 px-2 md:px-0">
      <router-view />
    </div>
    <PageFooter />
  </div>
</template>
