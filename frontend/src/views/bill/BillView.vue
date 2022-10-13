<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useBillStore } from '@/stores/bill';
import { useItemsStore } from '@/stores/items';
import { useParticipantsStore } from '@/stores/participants';
import BigCenteredScreen from '@/components/BigCenteredScreen.vue';
import ParticipantsSelector from './components/ParticipantsSelector.vue';
import NewParticipantModal from './components/NewParticipantModal.vue';
import ItemCard from './components/ItemCard.vue';

const billStore = useBillStore();
const itemsStore = useItemsStore();
const participantsStore = useParticipantsStore();
const router = useRouter();
const route = useRoute();

const loading = ref(false);

const newParticipantModalOpened = ref(false);
const creatingNewParticipant = ref(false);

const openNewParticipantModal = () => {
  newParticipantModalOpened.value = true;
};

const closeNewParticipantModal = () => {
  newParticipantModalOpened.value = false;
};

const createNewParticipant = async (name: string) => {
  if (billStore.bill) {
    creatingNewParticipant.value = true;
    await participantsStore.create(billStore.bill.id, name);
    creatingNewParticipant.value = false;
  }
  closeNewParticipantModal();
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
  <NewParticipantModal
    :show="newParticipantModalOpened"
    :creating="creatingNewParticipant"
    @create="createNewParticipant"
    @close="closeNewParticipantModal"
  />
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
    class="flex flex-col mt-4"
  >
    <div class="mx-4 border-b-2 text-center">
      <h1 class="mb-2 font-medium text-2xl text-gray-800">
        Participants
      </h1>
    </div>
    <ParticipantsSelector
      class="my-4"
      :participants="participantsStore.participants"
      :get-participant-color="participantsStore.getColor"
      @new-participant="openNewParticipantModal"
    />
    <div class="mx-4 mb-2 border-b-2 text-center">
      <h1 class="mb-2 font-medium text-2xl text-gray-800">
        Bill Items
      </h1>
    </div>
    <ItemCard
      v-for="item in itemsStore.items"
      :key="item.id"
      class="my-2"
      :item="item"
    />
  </div>
</template>
