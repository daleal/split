<script setup lang="ts">
import { computed } from 'vue';

import type { Item } from '@/types/api/item';

const props = defineProps<{ item: Item }>();

const formatter = Intl.NumberFormat('es-CL', {
  style: 'currency',
  currency: 'CLP',
});

const fullPrice = computed(() => formatter.format(props.item.fullPrice));
const individualPrice = computed(() => formatter.format(props.item.individualPrice));
</script>

<template>
  <div class="bg-gray-50 rounded-lg shadow-md">
    <div class="px-5 pt-2 pb-5">
      <h5 class="text-xl font-semibold tracking-tight text-gray-900">
        {{ props.item.description }}
      </h5>
      <div class="flex justify-between items-center pt-4">
        <div>
          <span class="text-2xl font-bold text-gray-900">{{ props.item.amount }}</span>
          <span class="text-lg font-semibold text-gray-900 pl-1">items</span>
        </div>
        <div>
          <span class="text-2xl font-bold text-gray-900">{{ fullPrice }}</span>
          <span class="text-lg font-semibold text-gray-900 pl-1">total</span>
        </div>
      </div>
      <div class="flex justify-end">
        <div class="pt-2">
          <span class="text-2xl font-bold text-gray-900">{{ individualPrice }}</span>
          <span class="text-lg font-semibold text-gray-900 pl-1">c/u</span>
        </div>
      </div>
    </div>
  </div>
</template>
