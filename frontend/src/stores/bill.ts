import { ref } from 'vue';
import { acceptHMRUpdate, defineStore } from 'pinia';
import * as api from '@/api';
import { RETRIES } from '@/constants/backend';
import { useImageUpload } from '@/composables/imageUpload';
import { useItemsStore } from '@/stores/items';

import type { Bill } from '@/types/api/bill';
import type { Nullable } from '@/types/utils';

export const useBillStore = defineStore('bill', () => {
  const itemsStore = useItemsStore();
  const { uploadImage, getUploadedImage } = useImageUpload();

  const loaded = ref(false);
  const bill = ref<Nullable<Bill>>(null);

  const insistentBillCreate = async () => {
    for (let iteration = 0; iteration < RETRIES; iteration += 1) {
      try {
        // eslint-disable-next-line no-await-in-loop
        const createdBill = await api.bills.create();
        return createdBill;
      } catch {} // eslint-disable-line no-empty
    }
    throw new Error('Bill failed to create');
  };

  const insistentBillLoad = async (billId: string) => {
    for (let iteration = 0; iteration < RETRIES; iteration += 1) {
      try {
        // eslint-disable-next-line no-await-in-loop
        const loadedBill = await api.bills.get(billId);
        return loadedBill;
      } catch {} // eslint-disable-line no-empty
    }
    throw new Error(`Bill ${billId} failed to load`);
  };

  const pollBillStatus = async (billId: string) => new Promise<Bill>((resolve) => {
    const interval = setInterval(async () => {
      const polledBill = await api.bills.get(billId);
      if (!polledBill.runningItemGeneration) {
        clearInterval(interval);
        resolve(polledBill);
      }
    }, 1000);
  });

  const create = async () => {
    bill.value = await api.bills.create();
  };

  const load = async (billId: string) => {
    if (!loaded.value) {
      bill.value = await insistentBillLoad(billId);
      loaded.value = true;
    }
  };

  const attachImage = async (billId: string) => {
    const image = await getUploadedImage();
    if (image) {
      await api.bills.attachImage(billId, image.url);
    }
  };

  const bootstrap = async (file: Nullable<File>) => {
    uploadImage(file); // Deliberately not awaited
    bill.value = await insistentBillCreate();
    await attachImage(bill.value.id);
    loaded.value = true;
    await itemsStore.generate(bill.value.id);
    bill.value = await pollBillStatus(bill.value.id);
  };

  return {
    bill, create, load, attachImage, bootstrap,
  };
});

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useBillStore, import.meta.hot));
}
