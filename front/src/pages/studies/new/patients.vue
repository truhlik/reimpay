<template>
  <div/>
</template>

<script>
  export default {
    name: "newPatients",
    created() {
      this.$router.push(this.localePath({name: 'studies-new-setup'}))
    }
  }
</script>
