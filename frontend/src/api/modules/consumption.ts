import { client } from '@/api/client';

import type { Consumption } from '@/types/api/consumption';

const BASE_PATH = (participantId: string) => `/participants/${participantId}/consumption`;

export const all = async (participantId: string) => {
  const response = await client.get<Array<Consumption>>(`${BASE_PATH(participantId)}`);
  return response.data;
};

export const createOrUpdate = async (participantId: string, itemId: string, amount: number) => {
  const response = await client.put<Consumption>(`${BASE_PATH(participantId)}/${itemId}`, { amount });
  return response.data;
};

export const remove = (participantId: string, itemId: string) => client.delete(`${BASE_PATH(participantId)}/${itemId}`);
