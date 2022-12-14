<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { colors } from '@/utils/colors';
import { consumptionAmountFormatter } from '@/utils/formatters';
import { numbersFormatter, parseFloat } from '@/utils/intl';
import TextBadge from '@/components/TextBadge.vue';
import GenericModal from '@/components/GenericModal.vue';
import GenericInput from '@/components/GenericInput.vue';
import GenericButton from '@/components/GenericButton.vue';

import type { Item } from '@/types/api/item';
import type { Participant } from '@/types/api/participant';
import { Nullable } from '@/types/utils';

const props = defineProps<{
  item: Nullable<Item>,
  selectedParticipant: Nullable<Participant>,
  selectedParticipantColor: Nullable<typeof colors[number]>,
  show: boolean,
  modifyingConsumption: boolean
}>();

const emit = defineEmits<{
  (e: 'modify-consumption', amount: number): void,
  (e: 'remove-consumption'): void,
  (e: 'close'): void
}>();

const consumption = computed(() => {
  if (props.selectedParticipant && props.item) {
    const participantId = props.selectedParticipant.id;
    return props.item.consumption.find((individualConsumption) => (
      individualConsumption.participantId === participantId
    )) || null;
  }
  return null;
});

const amount = ref(numbersFormatter.format(consumption.value?.amount || 0));

const removableConsumption = computed(() => (
  consumption.value && !parseFloat(amount.value)
));
const mainButtonType = computed(() => (removableConsumption.value ? 'danger' : 'primary'));
const mainButtonIcon = computed(() => (removableConsumption.value ? 'trash-can' : 'check'));

const showMainButton = computed(() => (
  removableConsumption.value || parseFloat(amount.value)
));

const modifyConsumption = () => {
  if (props.item) {
    const consumptionAmount = parseFloat(amount.value);
    if (!consumptionAmount && consumption.value !== null) {
      emit('remove-consumption');
    } else {
      emit('modify-consumption', consumptionAmount);
    }
  }
};

const close = () => {
  emit('close');
};

watch([() => props.item, () => props.selectedParticipant], () => {
  amount.value = numbersFormatter.format(consumption.value?.amount || 0);
});
</script>

<template>
  <GenericModal :show="props.show">
    <div class="flex flex-col">
      <h2
        v-if="props.item"
        class="border-b pb-1 mb-1.5 font-bold text-xl text-gray-700"
      >
        {{ props.item.description }}
      </h2>
      <div
        v-if="props.selectedParticipant && props.selectedParticipantColor"
        class="mb-3"
      >
        <span class="mr-1 font-semibold text-xl text-gray-700">
          Consumption by
        </span>
        <TextBadge
          class="mr-1"
          :text="props.selectedParticipant.name"
          :color="props.selectedParticipantColor"
        />
        <span class="font-semibold text-xl text-gray-700">
          was...
        </span>
      </div>
      <GenericInput
        v-model="amount"
        class="w-72 md:w-80"
        :disabled="props.modifyingConsumption"
        :loading="props.modifyingConsumption"
        :formatter="consumptionAmountFormatter"
      />
      <div class="mt-1 flex justify-end">
        <GenericButton
          type="secondary"
          :disabled="props.modifyingConsumption"
          @click="close"
        >
          <FontAwesomeIcon
            size="lg"
            :icon="[ 'fas', 'xmark' ]"
          />
        </GenericButton>
        <GenericButton
          v-if="showMainButton"
          class="ml-3"
          :type="mainButtonType"
          :disabled="props.modifyingConsumption"
          @click="modifyConsumption"
        >
          <FontAwesomeIcon :icon="[ 'fas', mainButtonIcon ]" />
        </GenericButton>
      </div>
    </div>
  </GenericModal>
</template>
