<script setup lang="ts">
import { ref, watch } from 'vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { zeroToHundreadIntergerFormatter } from '@/utils/formatters';
import GenericModal from '@/components/GenericModal.vue';
import GenericInput from '@/components/GenericInput.vue';
import GenericButton from '@/components/GenericButton.vue';

const props = defineProps<{
  value: string,
  show: boolean,
}>();

const emit = defineEmits<{
  (e: 'update-value', value: string): void,
  (e: 'close'): void,
}>();

const value = ref(props.value);

const updateValue = () => {
  emit('update-value', value.value);
};

const close = () => {
  emit('close');
};

watch(() => props.value, () => {
  value.value = props.value;
});
</script>

<template>
  <GenericModal :show="props.show">
    <div class="flex flex-col">
      <h2 class="mb-3 font-semibold text-xl text-gray-700">
        Enter the tip in %
      </h2>
      <GenericInput
        v-model="value"
        class="w-72 md:w-80"
        :formatter="zeroToHundreadIntergerFormatter"
      />
      <div class="mt-1 flex justify-end">
        <GenericButton
          type="secondary"
          @click="close"
        >
          <FontAwesomeIcon
            size="lg"
            :icon="[ 'fas', 'xmark' ]"
          />
        </GenericButton>
        <GenericButton
          class="ml-3"
          @click="updateValue"
        >
          <FontAwesomeIcon :icon="[ 'fas', 'check' ]" />
        </GenericButton>
      </div>
    </div>
  </GenericModal>
</template>
