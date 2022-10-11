<script setup lang="ts">
import * as cloudinary from '@/services/cloudinary';
import FileHandler from '@/components/FileHandler.vue';

import type { Nullable } from '@/types/utils';

const fileSelected = async (file: Nullable<File>) => {
  if (file) {
    const { url } = await cloudinary.upload(file);
    console.log(url);
  }
};
</script>

<template>
  <FileHandler @file-selected="fileSelected" />
</template>
