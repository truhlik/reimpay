import Vue from 'vue'

Vue.filter('errorToState', value => {
  if (value === undefined || value === null) return null;
  return !value;  // if value exists, return false meaning invalid input
});
