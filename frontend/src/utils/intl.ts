export const LOCALE = 'es-CL';

export const currencyFormatter = Intl.NumberFormat(LOCALE, {
  style: 'currency',
  currency: 'CLP',
});

export const numbersFormatter = Intl.NumberFormat(LOCALE);

export const parseFloat = (text: string) => Number.parseFloat(text.replace(',', '.'));
