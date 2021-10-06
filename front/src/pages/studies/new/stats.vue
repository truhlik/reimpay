<template>
  <div/>
</template>

<script>
  export default {
    name: "newStats",
    created() {
      this.$router.push(this.localePath({ name: 'studies-new-setup' }))
    }
  }
</script>
