export default function redirectToIndex(store) {
  // I had to create this workaround because of missing $router in Store interface
  store.$router.push({path: '/'});
}
