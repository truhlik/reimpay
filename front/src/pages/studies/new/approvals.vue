<template>
  <div/>
</template>

<script>
  export default {
    name: "newSummary",
    created() {
      this.$router.push(this.localePath({name: 'studies-new-setup'}))
    }
  }
</script>
