import { Consumption } from '@/types/api/consumption';

export interface Item {
  id: string,
  description: string,
  amount: number,
  fullPrice: number,
  individualPrice: number,
  consumption: Array<Consumption>,
}
