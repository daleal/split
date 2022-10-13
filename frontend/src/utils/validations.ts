export const validateNonEmpty = (errorMessage?: string) => (value: string) => {
  if (value.trim().length > 0) {
    return true;
  }
  return errorMessage || 'This field cannot be empty';
};

export const validateMinimumCharacterAmount = (
  characters: number,
  errorMessage?: string,
) => (value: string) => {
  if (value.trim().length >= characters) {
    return true;
  }
  return errorMessage || `This field needs to be at least ${characters} characters long`;
};
