<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useBillStore } from '@/stores/bill';
import { useItemsStore } from '@/stores/items';
import ItemCard from '@/components/ItemCard.vue';
import LoadingScreen from '@/components/LoadingScreen.vue';

const billStore = useBillStore();
const itemsStore = useItemsStore();
const router = useRouter();
const route = useRoute();

const loading = ref(false);

const fetchBill = async (billId: string) => {
  loading.value = true;
  try {
    const billPromise = billStore.load(billId);
    const itemsPromise = itemsStore.load(billId);
    await Promise.all([billPromise, itemsPromise]);
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
  <LoadingScreen v-if="loading" />
  <div
    v-else-if="!itemsStore.items"
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
      v-for="item in itemsStore.items"
      :key="item.id"
      :item="item"
    />
  </div>
</template>
