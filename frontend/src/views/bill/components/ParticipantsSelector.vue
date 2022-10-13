<script setup lang="ts">
import { colors } from '@/utils/colors';
import TextBadge from '@/components/TextBadge.vue';

import type { Participant } from '@/types/api/participant';

const props = defineProps<{
  participants: Array<Participant>,
  getParticipantColor: (participantId: string) => typeof colors[number],
}>();

const emit = defineEmits<{ (e: 'new-participant'): void }>();

const newParticipant = () => {
  emit('new-participant');
};
</script>

<template>
  <div class="w-full px-3 flex flex-wrap justify-center items-center space-between">
    <TextBadge
      v-for="participant in props.participants"
      :key="participant.id"
      class="mx-3 my-2"
      :text="participant.name"
      :color="getParticipantColor(participant.id)"
    />
    <TextBadge
      class="mx-3 my-2"
      text="+"
      @click="newParticipant"
    />
  </div>
</template>
