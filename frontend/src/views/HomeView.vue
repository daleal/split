<script setup lang="ts">
import { onUnmounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useBillStore } from '@/stores/bill';
import FileHandler from '@/components/FileHandler.vue';
import BigCenteredScreen from '@/components/BigCenteredScreen.vue';
import GenericSpinner from '@/components/GenericSpinner.vue';

import type { Nullable } from '@/types/utils';

const billStore = useBillStore();
const router = useRouter();

const loading = ref(false);
const showLoadingTip = ref(false);
const error = ref(false);

let tipTimeout: number | undefined;

const fileSelected = async (file: Nullable<File>) => {
  showLoadingTip.value = false;
  error.value = false;
  loading.value = true;
  tipTimeout = setTimeout(() => { showLoadingTip.value = true; }, 8000);
  try {
    await billStore.bootstrap(file);
    if (billStore.bill) {
      if (billStore.bill.generationSuccessful) {
        await router.push({ path: `/${billStore.bill.id}` });
      } else {
        error.value = true;
      }
    }
  } catch {
    error.value = true;
  } finally {
    clearTimeout(tipTimeout);
    loading.value = false;
  }
};

onUnmounted(() => { clearTimeout(tipTimeout); });
</script>

<template>
  <BigCenteredScreen v-if="loading">
    <GenericSpinner class="w-20 h-20 mx-auto text-gray-200 fill-purple-600" />
    <Transition
      enter-from-class="opacity-0"
      enter-active-class="transition duration-300"
    >
      <h3
        v-if="showLoadingTip"
        class="mt-20 mx-4 text-center font-bold text-xl text-purple-600"
      >
        This might take a couple of seconds. Don't panic!
      </h3>
    </Transition>
  </BigCenteredScreen>
  <FileHandler
    v-else
    class="mt-3"
    @file-selected="fileSelected"
  />
  <div
    v-if="error"
    class="mt-10 mx-4 text-center"
  >
    <h3 class="mb-2 font-semibold text-xl text-gray-600">
      Something went wrong! Please try uploading another image.
    </h3>
    <div v-if="billStore.bill">
      <h5
        v-if="billStore.bill.imageFound === false"
        class="mt-3 italic text-md text-gray-600"
      >
        There appears to have been an error when uploading the bill image.
      </h5>
      <h5
        v-else-if="billStore.bill.imageFound && billStore.bill.bordersDetected === false"
        class="mt-3 italic text-md text-gray-600"
      >
        There appears to have been an error when searching for the bill edges.
      </h5>
      <h5
        v-else-if="billStore.bill.imageFound && billStore.bill.bordersDetected"
        class="mt-3 italic text-md text-gray-600"
      >
        There appears to have been an error when extracting the text from the image.
      </h5>
      <h5 class="italic text-md text-gray-600">
        If you want more information, ask the developer about the
        bill with the following id:
      </h5>
      <h3 class="mt-1 font-extrabold text-md text-gray-600">
        {{ billStore.bill.id }}
      </h3>
    </div>
  </div>
</template>
