<script setup lang="ts">
import { watch } from 'vue';
import { useField } from 'vee-validate';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { validateNonEmpty, validateMinimumCharacterAmount } from '@/utils/validations';
import GenericModal from '@/components/GenericModal.vue';
import GenericInput from '@/components/GenericInput.vue';
import GenericButton from '@/components/GenericButton.vue';

const props = defineProps<{ show: boolean, creating: boolean }>();

const emit = defineEmits<{ (e: 'create', name: string): void, (e: 'close'): void }>();

const {
  value, errorMessage, resetField, meta,
} = useField('alias', [
  validateNonEmpty(),
  validateMinimumCharacterAmount(3),
], {
  initialValue: '',
});

const create = () => {
  emit('create', value.value);
};

const close = () => {
  emit('close');
};

watch(() => props.show, () => {
  if (!props.show) {
    resetField();
  }
});
</script>

<template>
  <GenericModal :show="props.show">
    <div class="flex flex-col">
      <GenericInput
        v-model="value"
        autocapitalize="none"
        :disabled="props.creating"
        :loading="props.creating"
        class="w-72 md:w-80"
        :error="errorMessage"
      />
      <div class="mt-1 flex justify-end">
        <GenericButton
          type="secondary"
          :disabled="props.creating"
          @click="close"
        >
          <FontAwesomeIcon
            size="lg"
            :icon="[ 'fas', 'xmark' ]"
          />
        </GenericButton>
        <GenericButton
          class="ml-3"
          :disabled="props.creating || !meta.valid"
          @click="create"
        >
          <FontAwesomeIcon :icon="[ 'fas', 'check' ]" />
        </GenericButton>
      </div>
    </div>
  </GenericModal>
</template>
