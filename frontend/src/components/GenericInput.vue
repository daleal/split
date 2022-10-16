<script setup lang="ts">
import { computed, toRef } from 'vue';
import GenericSpinner from '@/components/GenericSpinner.vue';

const props = withDefaults(defineProps<{
  modelValue: string,
  autocapitalize?: string,
  placeholder?: string,
  hint?: string,
  error?: string,
  loading?: boolean,
  disabled?: boolean,
  formatter?: (newValue: string, oldValue: string) => string,
}>(), {
  autocapitalize: 'sentences',
  loading: false,
  disabled: false,
  formatter: (value: string) => value,
});
const emit = defineEmits<{ (e: 'update:modelValue', value: string): void }>();
const value = toRef(props, 'modelValue');
const renderSubText = computed(() => !props.loading && (!!props.hint || !!props.error));
const subTextColorClasses = computed(() => {
  if (!props.loading && props.error) {
    return 'text-red-600';
  }
  return 'text-gray-600';
});
const inputColorClasses = computed(() => {
  if (!props.loading && props.error) {
    return 'border-red-200 focus:border-red-600';
  }
  return 'focus:border-gray-500';
});
const updateInput = (event: Event) => {
  const target = (event.target as HTMLInputElement);
  const formattedValue = props.formatter(target.value, props.modelValue);
  emit('update:modelValue', formattedValue);
  target.value = formattedValue;
};
</script>

<template>
  <div>
    <input
      :class="`
        focus:outline-none w-full border-2 rounded-md px-4 py-3
        leading-tight text-gray-900 placeholder-gray-400
        ${inputColorClasses} ${ !props.loading && !renderSubText ? 'mb-6' : '' }
        disabled:bg-gray-50 disabled:text-gray-500 disabled:border-gray-200 disabled:shadow-none
      `"
      :autocapitalize="props.autocapitalize"
      :placeholder="props.placeholder"
      :value="value"
      :disabled="props.disabled"
      @input="updateInput"
    >
    <GenericSpinner
      v-if="props.loading"
      class="mt-2 ml-1 w-4 h-4 text-gray-200 fill-purple-600"
    />
    <p
      v-if="renderSubText"
      :class="`pt-1 px-1 text-sm select-none ${subTextColorClasses}`"
    >
      {{ props.error || props.hint }}
    </p>
  </div>
</template>
