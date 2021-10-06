<template>
  <div/>
</template>

<script>
  export default {
    name: "newVisits",
    created() {
      this.$router.push(this.localePath({name: 'studies-new-setup'}))
    }
  }
</script>
