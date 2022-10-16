<script setup lang="ts">
import { computed } from 'vue';
import { colors } from '@/utils/colors';
import ConsumptionColors from '@/views/bill/components/consumption/ConsumptionColors.vue';

import type { Item } from '@/types/api/item';
import type { Participant } from '@/types/api/participant';
import type { Nullable } from '@/types/utils';

const props = defineProps<{
  item: Item,
  participant: Nullable<Participant>,
  getParticipantColor: (participantId: string) => typeof colors[number],
}>();

const emit = defineEmits<{ (e: 'modify-consumption', item?: Item): void }>();

const formatter = Intl.NumberFormat('es-CL', {
  style: 'currency',
  currency: 'CLP',
});

const fullPrice = computed(() => formatter.format(props.item.fullPrice));
const individualPrice = computed(() => formatter.format(props.item.individualPrice));
const amountConsumed = computed(
  () => props.item.consumption.reduce((total, consumption) => total + consumption.amount, 0),
);

const inflect = (word: string, amount: number) => (amount === 1 ? word : `${word}s`);

const modifyConsumption = () => {
  if (props.participant) {
    emit('modify-consumption', props.item);
  }
};
</script>

<template>
  <div class="bg-gray-50 rounded-lg shadow-md select-none">
    <div class="px-5 mt-2 mb-5">
      <h5 class="text-xl font-semibold tracking-tight text-gray-900">
        {{ props.item.description }}
      </h5>
      <div class="flex justify-between items-center mt-4">
        <div class="px-2">
          <span class="text-2xl font-bold text-gray-900">{{ fullPrice }}</span>
          <span class="text-lg font-semibold text-gray-900 ml-1">total</span>
        </div>
        <div class="px-2">
          <span class="text-2xl font-bold text-gray-900">{{ props.item.amount }}</span>
          <span class="text-lg font-semibold text-gray-900 ml-1">
            {{ inflect('item', props.item.amount) }}
          </span>
        </div>
      </div>
      <div class="flex justify-between items-center">
        <div class="px-2 mt-2">
          <span class="text-2xl font-bold text-gray-900">{{ individualPrice }}</span>
          <span class="text-lg font-semibold text-gray-900 ml-1">c/u</span>
        </div>
        <div
          class="border rounded-lg pt-0.5 pb-1 mt-2"
          :class="{
            'border-gray-50': !props.participant,
            'bg-white cursor-pointer': !!props.participant,
            'flex items-center pl-2 pr-1.5': item.consumption.length > 0,
            'px-2': !item.consumption.length,
          }"
          @click="modifyConsumption"
        >
          <span class="text-2xl font-bold text-gray-900">{{ amountConsumed }}</span>
          <ConsumptionColors
            v-if="item.consumption.length > 0"
            class="mt-1 ml-1"
            :consumption="item.consumption"
            :get-participant-color="props.getParticipantColor"
          />
          <span
            v-else
            class="text-lg font-semibold text-gray-900 ml-1"
          >consumed</span>
        </div>
      </div>
    </div>
  </div>
</template>
