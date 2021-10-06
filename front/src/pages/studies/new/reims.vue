<template>
  <div/>
</template>

<script>
  export default {
    name: "newItems",
    created() {
      this.$router.push(this.localePath({name: 'studies-new-setup'}))
    }
  }
</script>
