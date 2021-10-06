<template>
  <div class="d-flex align-items-center justify-content-between w-100">
    <div class="font-size-lg">{{ item.label }}</div>
    <v-btn :disabled="!item.enabled" @click="handlePatchStudy" color="primary">
      {{ $t('studies.setup.lock') }}
    </v-btn>
  </div>
</template>

<script>
  import { mapActions } from 'vuex'

  export default {
    name: 'PrelaunchCard',
    props: {
      item: {
        type: Object,
        required: true
      }
    },
    methods: {
      ...mapActions({
        patchStudy: 'studies/patchStudy'
      }),
      async handlePatchStudy() {
        try {
          await this.patchStudy({ status: 'PRELAUNCH' })
          this.$toast.success(this.$t('common.savedSuccessfully'))
        } catch (e) {
          this.$toast.error(e.message)
        }
      }
    }
  }
</script>

<style scoped>

</style>
