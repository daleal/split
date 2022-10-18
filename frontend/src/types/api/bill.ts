import type { Nullable } from '@/types/utils';

export interface Bill {
  id: string,
  image: Nullable<string>,
  runningItemGeneration: boolean,
  imageFound: Nullable<boolean>,
  bordersDetected: Nullable<boolean>,
  generationSuccessful: Nullable<boolean>,
}
