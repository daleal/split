export const consumptionAmountFormatter = (newValue: string, oldValue: string) => {
  const validAmountExpression = /^[0-9]+\.?[0-9]{0,2}$/;
  const cleaned = newValue.trim().replace(',', '.');
  if (!cleaned) {
    return '0';
  }
  if (validAmountExpression.test(cleaned)) {
    const trailingCharacter = cleaned.at(-1) === '.' ? '.' : '';
    return Number.parseFloat(cleaned).toString() + trailingCharacter;
  }
  return oldValue;
};
