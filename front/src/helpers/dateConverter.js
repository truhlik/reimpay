export function toProperDate (value) {
  // if backend uses values of YYYYMM, but we need MM/YYYY
  if (!value) return '';
  value = value.toString();
  if (value.includes('/')) return value;   // probably already OK, return as it is
  return value.substr(4, 5) + '/' + value.substring(0, 4);
}
