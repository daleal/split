<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import * as api from '@/api';
import { useImageUpload } from '@/composables/imageUpload';
import ItemCard from '@/components/ItemCard.vue';

import type { Bill } from '@/types/api/bill';
import type { Nullable } from '@/types/utils';

const router = useRouter();
const route = useRoute();
const { getUploadedImage } = useImageUpload();

const loading = ref(false);
const bill = ref<Nullable<Bill>>(null);

const bootstrapBill = async (billId: string) => {
  const image = await getUploadedImage();
  if (image) {
    await api.bills.attachImage(billId, image.url);
    return api.bills.generateItems(billId);
  }
  return null;
};

const fetchBill = async (billId: string) => {
  loading.value = true;
  try {
    bill.value = await api.bills.get(billId);
    if (bill.value.image === null) {
      bill.value = await bootstrapBill(billId);
    }
  } catch {
    await router.push({ path: '/' });
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  const billId = route.params.billId as string;
  fetchBill(billId);
});
</script>

<template>
  <div
    v-if="loading"
    class="w-screen h-screen flex flex-col justify-center text-center"
  >
    <h2 class="font-medium text-3xl text-gray-800">
      Loading...
    </h2>
  </div>
  <div
    v-else-if="!bill?.items"
    class="w-screen h-screen flex flex-col justify-center text-center"
  >
    <h2 class="font-medium text-3xl text-gray-800">
      Something went wrong!
    </h2>
  </div>
  <div
    v-else
    class="flex flex-col mt-2"
  >
    <ItemCard
      v-for="item in bill.items"
      :key="item.id"
      :item="item"
    />
  </div>
</template>
