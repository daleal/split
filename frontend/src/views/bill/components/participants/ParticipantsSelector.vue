<script setup lang="ts">
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { colors } from '@/utils/colors';
import TextBadge from '@/components/TextBadge.vue';
import GenericButton from '@/components/GenericButton.vue';

import type { Participant } from '@/types/api/participant';
import type { Nullable } from '@/types/utils';

const props = defineProps<{
  participants: Array<Participant>,
  selectedParticipantId: Nullable<string>,
  getParticipantColor: (participantId: string) => typeof colors[number],
}>();

const emit = defineEmits<{
  (e: 'new-participant'): void,
  (e: 'select-participant', participantId: string): void
}>();

const selectionState = (participant: Participant) => {
  if (!props.selectedParticipantId) {
    return undefined;
  }
  return props.selectedParticipantId === participant.id ? 'selected' : 'not-selected';
};

const newParticipant = () => {
  emit('new-participant');
};

const selectParticipant = (participantId: string) => {
  emit('select-participant', participantId);
};
</script>

<template>
  <div class="w-full px-3 flex flex-wrap justify-center items-center space-between">
    <TextBadge
      v-for="participant in props.participants"
      :key="participant.id"
      class="mx-3 my-2"
      :selection-state="selectionState(participant)"
      :text="participant.name"
      :color="getParticipantColor(participant.id)"
      selectable
      @click="() => selectParticipant(participant.id)"
    />
    <GenericButton
      class="mx-3 my-2"
      @click="newParticipant"
    >
      <FontAwesomeIcon :icon="[ 'fas', 'plus' ]" />
    </GenericButton>
  </div>
</template>
