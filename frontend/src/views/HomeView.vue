<script setup lang="ts">
import { useRouter } from 'vue-router';
import * as api from '@/api';
import { useImageUpload } from '@/composables/imageUpload';
import FileHandler from '@/components/FileHandler.vue';

import type { Nullable } from '@/types/utils';

const router = useRouter();
const { uploadImage } = useImageUpload();

const fileSelected = async (file: Nullable<File>) => {
  uploadImage(file); // Deliberately not awaited
  const bill = await api.bills.create();
  await router.push({ path: `/${bill.id}` });
};
</script>

<template>
  <FileHandler @file-selected="fileSelected" />
</template>
