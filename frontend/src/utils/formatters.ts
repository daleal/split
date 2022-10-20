import { numbersFormatter } from '@/utils/intl';

export const consumptionAmountFormatter = (newValue: string, oldValue: string) => {
  const validAmountExpression = /^[0-9]+,?[0-9]{0,2}$/;
  const cleaned = newValue.trim().replace('.', ',');
  if (!cleaned) {
    return '0';
  }
  if (validAmountExpression.test(cleaned)) {
    const trailingCharacter = cleaned.at(-1) === ',' ? ',' : '';
    return numbersFormatter.format(
      Number.parseFloat(cleaned.replace(',', '.')),
    ) + trailingCharacter;
  }
  return oldValue;
};

export const zeroToHundreadIntergerFormatter = (newValue: string, oldValue: string) => {
  const validAmountExpression = /^[0-9]{1,3}$/;
  const cleaned = newValue.trim();
  if (!cleaned) {
    return '0';
  }
  if (validAmountExpression.test(cleaned)) {
    const number = Math.min(100, Number.parseInt(cleaned, 10));
    return number.toString();
  }
  return oldValue;
};
