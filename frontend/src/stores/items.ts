import { ref } from 'vue';
import { acceptHMRUpdate, defineStore } from 'pinia';
import * as api from '@/api';

import type { Consumption } from '@/types/api/consumption';
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

  const addOrUpdateConsumption = (consumption: Consumption) => {
    const item = items.value.find((internalItem) => internalItem.id === consumption.itemId);
    if (item) {
      const itemConsumption = item.consumption.find(
        (internalConsumption) => internalConsumption.id === consumption.id,
      );
      if (itemConsumption) {
        itemConsumption.amount = consumption.amount;
      } else {
        item.consumption = [...item.consumption, consumption];
      }
    }
  };

  const removeConsumption = (participantId: string, itemId: string) => {
    const item = items.value.find((internalItem) => internalItem.id === itemId);
    if (item) {
      const itemConsumption = item.consumption.find(
        (internalConsumption) => internalConsumption.participantId === participantId,
      );
      const consumptionIndex = itemConsumption ? item.consumption.indexOf(itemConsumption) : -1;
      if (consumptionIndex > -1) {
        item.consumption.splice(consumptionIndex, 1);
      }
    }
  };

  return {
    items, generate, load, addOrUpdateConsumption, removeConsumption,
  };
});

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useItemsStore, import.meta.hot));
}
