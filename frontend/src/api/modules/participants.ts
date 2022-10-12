import { client } from '@/api/client';

import type { Participant } from '@/types/api/participant';

const BASE_PATH = (billId: string) => `/bills/${billId}/participants`;

export const all = async (billId: string) => {
  const response = await client.get<Array<Participant>>(`${BASE_PATH(billId)}`);
  return response.data;
};

export const create = async (billId: string, participantName: string) => {
  const response = await client.post<Participant>(`${BASE_PATH(billId)}`, { name: participantName });
  return response.data;
};
