<script setup lang="ts">
import { computed } from 'vue';

import { badgeColors } from '@/utils/colors';

const props = defineProps<{ text: string, color?: typeof badgeColors[number] }>();

const colors = computed(() => {
  if (props.color === 'blue') {
    return 'bg-blue-100 text-blue-800';
  }
  if (props.color === 'red') {
    return 'bg-red-100 text-red-800';
  }
  if (props.color === 'green') {
    return 'bg-green-100 text-green-800';
  }
  if (props.color === 'yellow') {
    return 'bg-yellow-100 text-yellow-800';
  }
  if (props.color === 'indigo') {
    return 'bg-indigo-100 text-indigo-800';
  }
  if (props.color === 'purple') {
    return 'bg-purple-100 text-purple-800';
  }
  if (props.color === 'pink') {
    return 'bg-pink-100 text-pink-800';
  }
  return 'bg-gray-100 text-gray-800';
});
</script>

<template>
  <span
    :class="`
      ${colors} text-lg font-medium px-2.5 py-0.5 rounded
    `"
  >
    {{ props.text }}
  </span>
</template>
