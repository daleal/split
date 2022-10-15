<script setup lang="ts">
import { colors } from '@/utils/colors';

import type { Consumption } from '@/types/api/consumption';

const props = defineProps<{
  consumption: Array<Consumption>,
  getParticipantColor: (participantId: string) => typeof colors[number],
}>();

const colorClass = (consumption: Consumption) => {
  const color = props.getParticipantColor(consumption.participantId);
  if (color === 'blue') {
    return 'bg-blue-100 border-blue-800';
  }
  if (color === 'red') {
    return 'bg-red-100 border-red-800';
  }
  if (color === 'green') {
    return 'bg-green-100 border-green-800';
  }
  if (color === 'yellow') {
    return 'bg-yellow-100 border-yellow-800';
  }
  if (color === 'indigo') {
    return 'bg-indigo-100 border-indigo-800';
  }
  if (color === 'purple') {
    return 'bg-purple-100 border-purple-800';
  }
  if (color === 'pink') {
    return 'bg-pink-100 border-pink-800';
  }
  return 'bg-gray-100 border-gray-800';
};

const translationClasses = (index: number) => (!index ? '' : '-ml-3');
</script>

<template>
  <div class="flex">
    <div
      v-for="individualConsumption, index in props.consumption"
      :key="individualConsumption.id"
      :class="`
        w-5 h-5 rounded-full border
        ${colorClass(individualConsumption)}
        ${translationClasses(index)}
      `"
    />
  </div>
</template>
