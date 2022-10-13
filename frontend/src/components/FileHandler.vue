<script setup lang="ts">
import { computed, ref } from 'vue';
import UploadSVG from '@/assets/images/svg/upload.svg?component';

import type { Nullable } from '@/types/utils';

const emit = defineEmits<{ (e: 'file-selected', file: Nullable<File>): void }>();

const highlighted = ref(false);

const borderColor = computed(() => (highlighted.value ? 'border-purple-500' : 'border-gray-300'));
const backgroundColor = computed(() => (highlighted.value ? 'bg-purple-50' : 'bg-gray-50'));

const onFileExplorerSelection = (event: Event) => {
  event.preventDefault();
  const { files } = event.target as HTMLInputElement;
  const uplodadedFile = files ? files[0] : null;
  emit('file-selected', uplodadedFile);
};

const onDrop = (event: DragEvent) => {
  event.preventDefault();
  highlighted.value = false;
  const uplodadedFile = event.dataTransfer?.files[0] || null;
  emit('file-selected', uplodadedFile);
};

const onDragLeave = (event: Event) => {
  event.preventDefault();
  highlighted.value = false;
};

const onDragEnter = (event: Event) => {
  event.preventDefault();
  highlighted.value = true;
};

const onDragOver = (event: Event) => {
  event.preventDefault();
  highlighted.value = true;
};
</script>

<template>
  <div class="w-full flex justify-center items-center p-2">
    <label
      for="dropzone-file"
      :class="`
        w-full h-64 flex flex-col justify-center items-center rounded-lg
        cursor-pointer border-dashed border-2 ${backgroundColor} ${borderColor}
      `"
      @dragenter="onDragEnter"
      @dragover="onDragOver"
      @dragleave="onDragLeave"
      @drop="onDrop"
    >
      <div class="flex flex-col justify-center items-center pt-5 pb-6">
        <UploadSVG class="mb-3 w-10 h-10 text-gray-400" />
        <p class="mb-2 text-sm text-gray-500">
          <span class="font-semibold">Click to upload</span> or drag and drop
        </p>
      </div>
      <input
        id="dropzone-file"
        type="file"
        class="hidden"
        @change="onFileExplorerSelection"
      >
    </label>
  </div>
</template>
