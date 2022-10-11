import axios from 'axios';
import { CLOUD_NAME, UPLOAD_PRESET, FOLDER } from '@/constants/cloudinary';

const BASE_URL = 'https://api.cloudinary.com/v1_1';

interface OriginalUploadResponse {
  secure_url: string,
}

export const upload = async (file: File) => {
  const data = new FormData();
  data.append('upload_preset', UPLOAD_PRESET);
  data.append('folder', FOLDER);
  data.append('file', file);
  const response = await axios.post<OriginalUploadResponse>(`${BASE_URL}/${CLOUD_NAME}/upload`, data);
  return { url: response.data.secure_url };
};
