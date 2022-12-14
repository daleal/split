import { computed, reactive, ref } from 'vue';
import { useStorage } from '@vueuse/core';
import { acceptHMRUpdate, defineStore } from 'pinia';
import { selectRandom } from '@/utils/arrays';
import { colors } from '@/utils/colors';
import * as api from '@/api';
import { useBillStore } from '@/stores/bill';

import type { Consumption } from '@/types/api/consumption';
import type { Participant } from '@/types/api/participant';

export const useParticipantsStore = defineStore('participants', () => {
  const billStore = useBillStore();

  const selectedParticipantsStorage = useStorage<Record<string, string | undefined>>('selected-participants', {});
  const loaded = ref(false);
  const participants = ref<Array<Participant>>([]);
  const participantColors = reactive<Record<string, typeof colors[number]>>({});

  const getColor = (participantId: string) => {
    if (participantColors[participantId] === undefined) {
      participantColors[participantId] = selectRandom(colors);
    }
    return participantColors[participantId];
  };

  const findById = (participantId: string) => (
    participants.value.find((participant) => participant.id === participantId)
  );

  const selectedParticipant = computed(() => {
    if (billStore.bill) {
      const participantId = selectedParticipantsStorage.value[billStore.bill.id] || '';
      return findById(participantId) || null;
    }
    return null;
  });

  const selectedParticipantColor = computed(() => (
    selectedParticipant.value
      ? getColor(selectedParticipant.value.id)
      : null
  ));

  const load = async (billId: string) => {
    if (!loaded.value) {
      participants.value = await api.participants.all(billId);
      loaded.value = true;
    }
  };

  const create = async (billId: string, name: string) => {
    if (billStore.bill) {
      const newParticipant = await api.participants.create(billId, name);
      selectedParticipantsStorage.value[billStore.bill.id] = newParticipant.id;
      participants.value = [...participants.value, newParticipant];
    }
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

  const addOrUpdateConsumption = (consumption: Consumption) => {
    const participant = findById(consumption.participantId);
    if (participant) {
      const participantConsumption = participant.consumption.find(
        (internalConsumption) => internalConsumption.id === consumption.id,
      );
      if (participantConsumption) {
        participantConsumption.amount = consumption.amount;
      } else {
        participant.consumption = [...participant.consumption, consumption];
      }
    }
  };

  const removeConsumption = (participantId: string, itemId: string) => {
    const participant = findById(participantId);
    if (participant) {
      const participantConsumption = participant.consumption.find(
        (internalConsumption) => internalConsumption.itemId === itemId,
      );
      const consumptionIndex = (
        participantConsumption ? participant.consumption.indexOf(participantConsumption) : -1
      );
      if (consumptionIndex > -1) {
        participant.consumption.splice(consumptionIndex, 1);
      }
    }
  };

  return {
    participants,
    findById,
    selectedParticipant,
    selectedParticipantColor,
    load,
    create,
    getColor,
    selectParticipant,
    addOrUpdateConsumption,
    removeConsumption,
  };
});

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useParticipantsStore, import.meta.hot));
}
