import { acceptHMRUpdate, defineStore } from 'pinia';
import * as api from '@/api';
import { useItemsStore } from '@/stores/items';
import { useParticipantsStore } from '@/stores/participants';

import type { Consumption } from '@/types/api/consumption';

export const useConsumptionStore = defineStore('consumption', () => {
  const itemsStore = useItemsStore();
  const participantsStore = useParticipantsStore();

  const updateOrAddConsumption = async (consumption: Consumption) => {
    itemsStore.addOrUpdateConsumption(consumption);
    participantsStore.addOrUpdateConsumption(consumption);
  };

  const modifyConsumption = async (itemId: string, amount: number) => {
    if (participantsStore.selectedParticipant) {
      const consumption = await api.consumption.createOrUpdate(
        participantsStore.selectedParticipant.id,
        itemId,
        amount,
      );
      updateOrAddConsumption(consumption);
    }
  };

  const removeConsumption = async (itemId: string) => {
    if (participantsStore.selectedParticipant) {
      await api.consumption.remove(
        participantsStore.selectedParticipant.id,
        itemId,
      );
      itemsStore.removeConsumption(participantsStore.selectedParticipant.id, itemId);
      participantsStore.removeConsumption(participantsStore.selectedParticipant.id, itemId);
    }
  };

  return { modifyConsumption, removeConsumption };
});

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useConsumptionStore, import.meta.hot));
}
