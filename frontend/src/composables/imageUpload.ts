import { ref } from 'vue';
import * as cloudinary from '@/services/cloudinary';

import type { Nullable } from '@/types/utils';

const image = ref<Nullable<Promise<{ url: string }>>>(null);

const uploadImage = async (file: Nullable<File>) => {
  if (file) {
    image.value = cloudinary.upload(file);
  }
};

const getUploadedImage = async () => image.value;

export const useImageUpload = () => ({ uploadImage, getUploadedImage });
