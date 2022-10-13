<script setup lang="ts">
import { computed } from 'vue';
import { ButtonType } from '@/types/button';

const props = withDefaults(defineProps<{
  type?: typeof ButtonType[number],
  fullWidth?: boolean,
}>(), {
  type: 'primary',
  fullWidth: false,
});
const emit = defineEmits<{ (e: 'click'): void }>();
const widthClasses = computed(() => (props.fullWidth ? 'w-full' : ''));
const colorClasses = computed(() => {
  if (props.type === 'primary') {
    return 'text-white bg-purple-600 hover:bg-purple-500 disabled:bg-purple-300';
  } if (props.type === 'secondary') {
    return 'text-purple-600 bg-gray-300 hover:bg-gray-200 disabled:bg-gray-200 disabled:text-gray-400';
  }
  return '';
});
const onClick = () => {
  emit('click');
};
</script>

<template>
  <button
    :class="`
        px-3 py-1.5 rounded-md font-medium select-none text-center
        disabled:cursor-not-allowed
        ${widthClasses} ${colorClasses}
      `"
    @click="onClick"
  >
    <slot />
  </button>
</template>
