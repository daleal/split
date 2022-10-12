import { client } from '@/api/client';

import type { Item } from '@/types/api/item';

const BASE_PATH = (billId: string) => `/bills/${billId}/items`;

export const all = async (billId: string) => {
  const response = await client.get<Array<Item>>(`${BASE_PATH(billId)}`);
  return response.data;
};

export const generate = async (billId: string) => {
  const response = await client.post<Array<Item>>(`${BASE_PATH(billId)}/generate`);
  return response.data;
};
