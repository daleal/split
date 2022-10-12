import type { Item } from '@/types/api/item';
import type { Nullable } from '@/types/utils';

export interface Bill {
  id: string,
  image: Nullable<string>,
  items: Array<Item>,
}
