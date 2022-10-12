import { ref } from 'vue';
import { acceptHMRUpdate, defineStore } from 'pinia';
import * as api from '@/api';

import type { Item } from '@/types/api/item';

export const useItemsStore = defineStore('items', () => {
  const loaded = ref(false);
  const items = ref<Array<Item>>([]);

  const load = async (billId: string) => {
    if (!loaded.value) {
      items.value = await api.items.all(billId);
      loaded.value = true;
    }
  };

  const generate = async (billId: string) => {
    items.value = await api.items.generate(billId);
    loaded.value = true;
  };

  return { items, generate, load };
});

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useItemsStore, import.meta.hot));
}
