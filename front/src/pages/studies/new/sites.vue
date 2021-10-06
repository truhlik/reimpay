<template>
  <div/>
</template>

<script>
  export default {
    name: "newSites",
    created() {
      this.$router.push(this.localePath({name: 'studies-new-setup'}))
    }
  }
</script>
