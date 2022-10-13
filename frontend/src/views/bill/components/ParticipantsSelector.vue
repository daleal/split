<script setup lang="ts">
import { reactive } from 'vue';
import { selectRandom } from '@/utils/arrays';
import { badgeColors } from '@/utils/colors';
import TextBadge from '@/components/TextBadge.vue';

import type { Participant } from '@/types/api/participant';

const props = defineProps<{ participants: Array<Participant> }>();

const emit = defineEmits<{ (e: 'new-participant'): void }>();

const colors = reactive<Record<string, typeof badgeColors[number]>>({});

const getColor = (participantId: string) => {
  if (colors[participantId] === undefined) {
    colors[participantId] = selectRandom(badgeColors);
  }
  return colors[participantId];
};

const newParticipant = () => {
  emit('new-participant');
};
</script>

<template>
  <div class="w-full py-6 px-3 flex flex-wrap justify-center items-center space-between">
    <TextBadge
      v-for="participant in props.participants"
      :key="participant.id"
      class="mx-3 my-2"
      :text="participant.name"
      :color="getColor(participant.id)"
    />
    <TextBadge
      class="mx-3"
      text="+"
      @click="newParticipant"
    />
  </div>
</template>
