<script setup lang="ts">
import { computed, ref } from 'vue';
import { useItemsStore } from '@/stores/items';
import { useParticipantsStore } from '@/stores/participants';
import { currencyFormatter } from '@/utils/intl';
import TipModal from '@/views/bill/components/summary/TipModal.vue';
import GenericButton from '@/components/GenericButton.vue';

const itemsStore = useItemsStore();
const participantsStore = useParticipantsStore();

const show = computed(() => !!participantsStore.selectedParticipant?.consumption?.length);
const showTipModal = ref(false);
const tip = ref('10');

const toggleTipModal = () => {
  showTipModal.value = !showTipModal.value;
};

const updateTipValue = (newValue: string) => {
  tip.value = newValue;
  toggleTipModal();
};

const totalAmount = computed(() => {
  if (!participantsStore.selectedParticipant?.consumption?.length) {
    return 0;
  }
  const totalSpent = participantsStore.selectedParticipant.consumption.reduce(
    (amount, individualConsumption) => {
      const item = itemsStore.findById(individualConsumption.itemId);
      return amount + (individualConsumption.amount * (item?.individualPrice || 0));
    },
    0,
  );
  return totalSpent * ((100 + Number.parseInt(tip.value, 10)) / 100);
});
</script>

<template>
  <TipModal
    :value="tip"
    :show="showTipModal"
    @update-value="updateTipValue"
    @close="toggleTipModal"
  />
  <Teleport to=".main-container">
    <Transition
      enter-from-class="translate-y-[150%] opacity-0"
      enter-active-class="transition duration-300"
      leave-to-class="translate-y-[150%] opacity-0"
      leave-active-class="transition duration-300"
    >
      <div
        v-if="show"
        class="sticky bottom-0 w-full bg-white border-t-4 border-purple-500"
      >
        <div class="container max-w-md mx-auto my-6 px-5 md:px-0">
          <div class="flex items-center justify-between">
            <h2 class="font-bold text-2xl text-gray-800">
              Total owed: {{ currencyFormatter.format(totalAmount) }}
            </h2>
            <GenericButton
              @click="toggleTipModal"
            >
              Tip: {{ tip }}%
            </GenericButton>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>
