<template>
  <v-app class="app-container app-theme-white">
    <transition name="fade" mode="out-in" appear>
      <Header/>
    </transition>
    <transition name="fade" mode="out-in" appear>
      <Sidebar/>
    </transition>
    <div class="app-main__outer">
      <v-container class="app-main__inner ml-sm-3">
        <Nuxt/>
      </v-container>
    </div>
  </v-app>
</template>

<script>
  import Header from "../components/Header";
  import Sidebar from "../components/Sidebar";
  import VuePerfectScrollbar from 'vue-perfect-scrollbar'

  export default {
    name: 'app',
    components: {
      Header,
      Sidebar,
      VuePerfectScrollbar,
    },
    watch: {
    '$route.path': function() {
        this.$store.commit('errors/clearErrorObject')
      }
    },
  }
</script>

<style lang="scss">


</style>
