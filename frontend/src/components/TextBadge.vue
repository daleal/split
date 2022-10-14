<script setup lang="ts">
import { computed } from 'vue';
import { colors } from '@/utils/colors';
import { TextBadgeSelection } from '@/types/textBadge';

const props = withDefaults(defineProps<{
  text: string,
  selectable?: boolean,
  selectionState?: typeof TextBadgeSelection[number],
  color?: typeof colors[number]
}>(), {
  selectable: false,
});

const selectableClass = computed(() => (props.selectable ? 'cursor-pointer' : ''));

const selectionClass = computed(() => {
  if (props.selectionState === 'selected') {
    return 'border-2';
  }
  if (props.selectionState === 'not-selected') {
    return 'opacity-60';
  }
  return '';
});

const colorClasses = computed(() => {
  if (props.color === 'blue') {
    return 'bg-blue-100 border-blue-800 text-blue-800';
  }
  if (props.color === 'red') {
    return 'bg-red-100 border-red-800 text-red-800';
  }
  if (props.color === 'green') {
    return 'bg-green-100 border-green-800 text-green-800';
  }
  if (props.color === 'yellow') {
    return 'bg-yellow-100 border-yellow-800 text-yellow-800';
  }
  if (props.color === 'indigo') {
    return 'bg-indigo-100 border-indigo-800 text-indigo-800';
  }
  if (props.color === 'purple') {
    return 'bg-purple-100 border-purple-800 text-purple-800';
  }
  if (props.color === 'pink') {
    return 'bg-pink-100 border-pink-800 text-pink-800';
  }
  return 'bg-gray-100 border-gray-800 text-gray-800';
});
</script>

<template>
  <span
    :class="`
      ${colorClasses} ${selectableClass} text-lg font-medium
      ${selectionClass} select-none px-2.5 py-0.5 rounded
    `"
  >
    {{ props.text }}
  </span>
</template>
