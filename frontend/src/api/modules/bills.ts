import { client } from '@/api/client';

import type { Bill } from '@/types/api/bill';

const BASE_PATH = '/bills';

export const create = async () => {
  const response = await client.post<Bill>(BASE_PATH);
  return response.data;
};

export const get = async (billId: string) => {
  const response = await client.get<Bill>(`${BASE_PATH}/${billId}`);
  return response.data;
};

export const attachImage = async (billId: string, image: string) => {
  const response = await client.post<Bill>(`${BASE_PATH}/${billId}/image`, { image });
  return response.data;
};

export const generateItems = async (billId: string) => {
  const response = await client.post<Bill>(`${BASE_PATH}/${billId}/items`);
  return response.data;
};
