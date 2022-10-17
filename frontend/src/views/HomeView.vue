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
const error = ref(false);

const fileSelected = async (file: Nullable<File>) => {
  error.value = false;
  loading.value = true;
  try {
    await billStore.bootstrap(file);
    if (billStore.bill) {
      if (billStore.bill.generationSuccessful) {
        await router.push({ path: `/${billStore.bill.id}` });
      } else {
        error.value = true;
      }
    }
  } finally {
    loading.value = false;
    error.value = true;
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
  <h3
    v-if="error"
    class="mt-10 mx-4 text-center font-semibold text-xl text-gray-600"
  >
    Something went wrong! Please try uploading another image
  </h3>
</template>
