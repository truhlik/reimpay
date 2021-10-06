<template>
  <v-row>
    <v-col class="text-center">
      <nuxt-link :to="localePath({name: 'studies-id-setup', params: $route.params.id})">
        <v-btn color="primary" tabindex="-1" x-large>
          {{ $t('studies.doneBackToWizard') }}
        </v-btn>
      </nuxt-link>
    </v-col>
  </v-row>
</template>

<script>
  export default {
    name: 'DoneButtonRow'
  }
</script>
