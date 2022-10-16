import { computed, reactive, ref } from 'vue';
import { useStorage } from '@vueuse/core';
import { acceptHMRUpdate, defineStore } from 'pinia';
import { selectRandom } from '@/utils/arrays';
import { colors } from '@/utils/colors';
import * as api from '@/api';
import { useBillStore } from '@/stores/bill';

import type { Participant } from '@/types/api/participant';

export const useParticipantsStore = defineStore('participants', () => {
  const billStore = useBillStore();

  const selectedParticipantsStorage = useStorage<Record<string, string | undefined>>('selected-participants', {});
  const loaded = ref(false);
  const participants = ref<Array<Participant>>([]);
  const participantColors = reactive<Record<string, typeof colors[number]>>({});

  const selectedParticipantId = computed(() => {
    if (billStore.bill) {
      return selectedParticipantsStorage.value[billStore.bill.id] || null;
    }
    return null;
  });

  const load = async (billId: string) => {
    if (!loaded.value) {
      participants.value = await api.participants.all(billId);
      loaded.value = true;
    }
  };

  const create = async (billId: string, name: string) => {
    const newParticipant = await api.participants.create(billId, name);
    participants.value = [...participants.value, newParticipant];
  };

  const selectParticipant = (participantId: string) => {
    if (billStore.bill) {
      if (selectedParticipantsStorage.value[billStore.bill.id] === participantId) {
        selectedParticipantsStorage.value[billStore.bill.id] = undefined;
      } else {
        selectedParticipantsStorage.value[billStore.bill.id] = participantId;
      }
    }
  };

  const modifyConsumption = async (itemId: string, amount: number) => {
    if (selectedParticipantId.value) {
      await api.consumption.createOrUpdate(
        selectedParticipantId.value,
        itemId,
        amount,
      );
    }
  };

  const removeConsumption = async (itemId: string) => {
    if (selectedParticipantId.value) {
      await api.consumption.remove(
        selectedParticipantId.value,
        itemId,
      );
    }
  };

  const getColor = (participantId: string) => {
    if (participantColors[participantId] === undefined) {
      participantColors[participantId] = selectRandom(colors);
    }
    return participantColors[participantId];
  };

  return {
    participants,
    selectedParticipantId,
    load,
    create,
    getColor,
    selectParticipant,
    modifyConsumption,
    removeConsumption,
  };
});

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useParticipantsStore, import.meta.hot));
}
