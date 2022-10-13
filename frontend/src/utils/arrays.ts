export const selectRandom = <ElementsType>(
  array: Array<ElementsType> | readonly ElementsType[],
) => {
  const randomIndex = Math.floor(Math.random() * array.length);
  return array[randomIndex];
};
