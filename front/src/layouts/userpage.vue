<template>
  <v-app class="app-container app-theme-white">
    <Nuxt/>
  </v-app>
</template>

<script>

  export default {
    name: 'app',
    components: {
    },
    data() {
      return {
      }
    },
    methods:{

    },
    // middleware: 'notAuthenticated'
  }
</script>

<style>
  .app-login-box img.logo {
    display: block;
    margin: 30px auto 10px;
    max-width: 80%;
    width: 320px;
  }
</style>
