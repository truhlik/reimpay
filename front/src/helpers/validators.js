export function validateDummy(value) {
  if (value === undefined || value === null) return {state: null, valid: true};
  return {state: true, valid: true};
}

export function validateEmail(value) {
  if (value === undefined || value === null) return {state: null, valid: false};
  const regex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  const valid = regex.test(value.toLowerCase());
  return {state: valid, valid: valid};
}

export function validatePassword(value) {
  if (value === undefined || value === null) return {state: null, valid: false};
  const valid = value.length > 5;
  return {state: valid, valid: valid};
}

export function validatePasswordConfirm(value, passwordValue) {
  if (value === undefined || value === null) return {state: null, valid: false};
  const valid = value.length > 5 && value === passwordValue;
  return {state: valid, valid: valid};
}

export function validateRequiredField(value) {
  if (value === undefined) return {state: null, valid: false};
  return {state: !!value, valid: !!value};
}

export function validateRequiredIfField(value, condition) {
  if (value === undefined || !condition) return {state: null, valid: true};
  return {state: !!value, valid: !!value};
}

export function validateBetween(value, minValue, maxValue) {
  if (value === undefined) return {state: null, valid: false};
  const valid = minValue <= value && value <= maxValue;
  return {state: !!valid, valid: !!valid};
}
