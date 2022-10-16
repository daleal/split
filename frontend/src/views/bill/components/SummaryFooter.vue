<script setup lang="ts">
import { computed } from 'vue';
import { useItemsStore } from '@/stores/items';
import { useParticipantsStore } from '@/stores/participants';

const itemsStore = useItemsStore();
const participantsStore = useParticipantsStore();

const show = computed(() => !!participantsStore.selectedParticipant?.consumption?.length);

const totalAmount = computed(() => {
  if (!participantsStore.selectedParticipant?.consumption?.length) {
    return 0;
  }
  return participantsStore.selectedParticipant.consumption.reduce(
    (amount, individualConsumption) => {
      const item = itemsStore.findById(individualConsumption.itemId);
      return individualConsumption.amount * (amount + (item?.individualPrice || 0));
    },
    0,
  );
});
</script>

<template>
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
        <div class="container max-w-md mx-auto px-2 md:px-0">
          <h2 class="font-bold text-3xl text-gray-800 my-4">
            Total owed: {{ totalAmount }}
          </h2>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>
