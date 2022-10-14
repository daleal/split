import { Consumption } from '@/types/api/consumption';

export interface Participant {
  id: string,
  name: string,
  consumption: Array<Consumption>,
}
