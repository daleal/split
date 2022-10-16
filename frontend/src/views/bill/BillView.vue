<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useBillStore } from '@/stores/bill';
import { useConsumptionStore } from '@/stores/consumption';
import { useItemsStore } from '@/stores/items';
import { useParticipantsStore } from '@/stores/participants';
import BigCenteredScreen from '@/components/BigCenteredScreen.vue';
import GenericSpinner from '@/components/GenericSpinner.vue';
import ParticipantsSelector from '@/views/bill/components/participants/ParticipantsSelector.vue';
import NewParticipantModal from '@/views/bill/components/participants/NewParticipantModal.vue';
import ConsumptionModal from '@/views/bill/components/consumption/ConsumptionModal.vue';
import ItemCard from '@/views/bill/components/ItemCard.vue';
import SummaryFooter from '@/views/bill/components/SummaryFooter.vue';

import type { Item } from '@/types/api/item';
import type { Nullable } from '@/types/utils';

const billStore = useBillStore();
const consumptionStore = useConsumptionStore();
const itemsStore = useItemsStore();
const participantsStore = useParticipantsStore();
const router = useRouter();
const route = useRoute();

const loading = ref(false);

const newParticipantModalOpened = ref(false);
const creatingNewParticipant = ref(false);

const consumptionModalOpened = ref(false);
const selectedConsumptionItem = ref<Nullable<Item>>(null);
const modifyingConsumption = ref(false);

const toggleNewParticipantModal = () => {
  newParticipantModalOpened.value = !newParticipantModalOpened.value;
};

const createNewParticipant = async (name: string) => {
  if (billStore.bill) {
    creatingNewParticipant.value = true;
    await participantsStore.create(billStore.bill.id, name);
    creatingNewParticipant.value = false;
  }
  toggleNewParticipantModal();
};

const toggleConsumptionModal = (item?: Item) => {
  consumptionModalOpened.value = !consumptionModalOpened.value;
  selectedConsumptionItem.value = item || null;
};

const modifyConsumption = async (amount: number) => {
  if (selectedConsumptionItem.value) {
    modifyingConsumption.value = true;
    await consumptionStore.modifyConsumption(selectedConsumptionItem.value.id, amount);
    modifyingConsumption.value = false;
    toggleConsumptionModal();
  }
};

const removeConsumption = async () => {
  if (selectedConsumptionItem.value) {
    modifyingConsumption.value = true;
    try {
      await consumptionStore.removeConsumption(selectedConsumptionItem.value.id);
    } finally {
      modifyingConsumption.value = false;
      toggleConsumptionModal();
    }
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
  <NewParticipantModal
    :show="newParticipantModalOpened"
    :creating="creatingNewParticipant"
    @create="createNewParticipant"
    @close="toggleNewParticipantModal"
  />
  <ConsumptionModal
    :item="selectedConsumptionItem"
    :selected-participant="participantsStore.selectedParticipant"
    :show="consumptionModalOpened"
    :modifying-consumption="modifyingConsumption"
    @modify-consumption="modifyConsumption"
    @remove-consumption="removeConsumption"
    @close="toggleConsumptionModal"
  />
  <BigCenteredScreen v-if="loading">
    <GenericSpinner class="w-20 h-20 mx-auto text-gray-200 fill-purple-600" />
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
      :selected-participant="participantsStore.selectedParticipant"
      :get-participant-color="participantsStore.getColor"
      @select-participant="participantsStore.selectParticipant"
      @new-participant="toggleNewParticipantModal"
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
      :participant="participantsStore.selectedParticipant"
      :get-participant-color="participantsStore.getColor"
      @modify-consumption="toggleConsumptionModal"
    />
  </div>
  <SummaryFooter />
</template>
