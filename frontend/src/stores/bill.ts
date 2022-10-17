import { ref } from 'vue';
import { acceptHMRUpdate, defineStore } from 'pinia';
import * as api from '@/api';
import { useImageUpload } from '@/composables/imageUpload';
import { useItemsStore } from '@/stores/items';

import type { Bill } from '@/types/api/bill';
import type { Nullable } from '@/types/utils';

export const useBillStore = defineStore('bill', () => {
  const itemsStore = useItemsStore();
  const { uploadImage, getUploadedImage } = useImageUpload();

  const loaded = ref(false);
  const bill = ref<Nullable<Bill>>(null);

  const pollBillStatus = async (billId: string) => new Promise<Bill>((resolve) => {
    const interval = setInterval(async () => {
      const polledBill = await api.bills.get(billId);
      if (!polledBill.generatingItems) {
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
      bill.value = await api.bills.get(billId);
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
    bill.value = await api.bills.create();
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
