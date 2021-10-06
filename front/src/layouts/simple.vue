<template>
  <v-app class="app-container app-theme-white">
    <transition name="fade" mode="out-in" appear>
      <HeaderSimple/>
    </transition>
    <div class="app-main__outer">
      <v-container class="app-main__inner ml-sm-3">
        <Nuxt/>
      </v-container>
    </div>
  </v-app>
</template>

<script>
  import HeaderSimple from '~/components/HeaderSimple'

  export default {
    name: 'app',
    components: { HeaderSimple },
  }
</script>

<style lang="scss">


</style>
