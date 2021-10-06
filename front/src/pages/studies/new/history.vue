<template>
  <div/>
</template>

<script>
  export default {
    name: "newHistory",
    created() {
      this.$router.push(this.localePath({name: 'studies-new-setup'}))
    }
  }
</script>
