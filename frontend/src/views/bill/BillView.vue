<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useBillStore } from '@/stores/bill';
import { useItemsStore } from '@/stores/items';
import { useParticipantsStore } from '@/stores/participants';
import BigCenteredScreen from '@/components/BigCenteredScreen.vue';
import ParticipantsSelector from './components/ParticipantsSelector.vue';
import ItemCard from './components/ItemCard.vue';

const billStore = useBillStore();
const itemsStore = useItemsStore();
const participantsStore = useParticipantsStore();
const router = useRouter();
const route = useRoute();

const loading = ref(false);

const createNewParticipant = () => {
  if (billStore.bill) {
    participantsStore.create(billStore.bill.id, 'DIOS');
  }
};

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
  <BigCenteredScreen v-if="loading">
    <h2 class="font-medium text-3xl text-gray-800">
      Loading...
    </h2>
  </BigCenteredScreen>
  <BigCenteredScreen v-else-if="!itemsStore.items">
    <h2 class="font-medium text-3xl text-gray-800">
      Something went wrong!
    </h2>
  </BigCenteredScreen>
  <div
    v-else
    class="flex flex-col mt-2"
  >
    <ParticipantsSelector
      class="mb-2"
      :participants="participantsStore.participants"
      @new-participant="createNewParticipant"
    />
    <ItemCard
      v-for="item in itemsStore.items"
      :key="item.id"
      class="mb-4"
      :item="item"
    />
  </div>
</template>
