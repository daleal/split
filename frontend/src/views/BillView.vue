<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useBillStore } from '@/stores/bill';
import { useItemsStore } from '@/stores/items';
import { useParticipantsStore } from '@/stores/participants';
import ItemCard from '@/components/ItemCard.vue';
import LoadingScreen from '@/components/LoadingScreen.vue';

const billStore = useBillStore();
const itemsStore = useItemsStore();
const participantsStore = useParticipantsStore();
const router = useRouter();
const route = useRoute();

const loading = ref(false);

const loadBillData = async (billId: string) => {
  loading.value = true;
  try {
    const billPromise = billStore.load(billId);
    const itemsPromise = itemsStore.load(billId);
    const participantsPromise = participantsStore.load(billId);
    await Promise.all([billPromise, itemsPromise, participantsPromise]);
  } catch {
    await router.push({ path: '/' });
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  const billId = route.params.billId as string;
  loadBillData(billId);
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
    class="flex flex-col mt-6"
  >
    <ItemCard
      v-for="item in itemsStore.items"
      :key="item.id"
      class="mb-4"
      :item="item"
    />
  </div>
</template>
