import { ref } from 'vue';
import { acceptHMRUpdate, defineStore } from 'pinia';
import * as api from '@/api';

import type { Participant } from '@/types/api/participant';

export const useParticipantsStore = defineStore('participants', () => {
  const loaded = ref(false);
  const participants = ref<Array<Participant>>([]);

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

  return { participants, load, create };
});

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useParticipantsStore, import.meta.hot));
}
