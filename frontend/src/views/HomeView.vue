<script setup lang="ts">
import { ref } from 'vue';
import * as cloudinary from '@/services/cloudinary';
import FileHandler from '@/components/FileHandler.vue';

import type { Nullable } from '@/types/utils';

const uploadedUrl = ref('');

const fileSelected = async (file: Nullable<File>) => {
  if (file) {
    const { url } = await cloudinary.upload(file);
    uploadedUrl.value = url;
  }
};
</script>

<template>
  <FileHandler @file-selected="fileSelected" />

  <div
    v-if="uploadedUrl"
    class="w-full text-center mt-4"
  >
    <a
      :href="uploadedUrl"
      class="font-medium text-fuchsia-500 hover:underline"
      target="_blank"
    >
      Ver imagen!
    </a>
  </div>
</template>
