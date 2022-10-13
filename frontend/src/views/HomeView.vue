<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useBillStore } from '@/stores/bill';
import FileHandler from '@/components/FileHandler.vue';
import BigCenteredScreen from '@/components/BigCenteredScreen.vue';
import GenericSpinner from '@/components/GenericSpinner.vue';

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
  <BigCenteredScreen v-if="loading">
    <GenericSpinner class="w-20 h-20 mx-auto text-gray-200 fill-purple-600" />
  </BigCenteredScreen>
  <FileHandler
    v-else
    class="mt-3"
    @file-selected="fileSelected"
  />
</template>
