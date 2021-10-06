<template>
  <div/>
</template>

<script>
  export default {
    name: "newFinance",
    created() {
      this.$router.push(this.localePath({name: 'studies-new-setup'}))
    }
  }
</script>
