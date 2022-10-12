<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useBillStore } from '@/stores/bill';
import FileHandler from '@/components/FileHandler.vue';
import LoadingScreen from '@/components/LoadingScreen.vue';

import type { Nullable } from '@/types/utils';

const billStore = useBillStore();
const router = useRouter();

const loading = ref(false);

const fileSelected = async (file: Nullable<File>) => {
  loading.value = true;
  try {
    await billStore.bootstrap(file);
    if (billStore.bill) {
      await router.push({ path: `/${billStore.bill.id}` });
    }
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <LoadingScreen v-if="loading" />
  <FileHandler
    v-else
    @file-selected="fileSelected"
  />
</template>
