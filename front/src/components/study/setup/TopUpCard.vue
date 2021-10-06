<template>
  <div>
    <div class="font-size-lg">{{ item.label }}</div>
    <div class="d-flex flex-wrap justify-content-center pt-4 w-100">
      <div class="w-50">
        <p><b><i>{{ $t('studies.setup.step6minimalTopup') }}</i></b></p>
        <p><b><i>{{ $t('studies.setup.step6furtherTopup') }}</i></b></p>
      </div>
      <div class="w-50">

      </div>
      <div class="d-flex justify-content-center w-100">
        <v-btn :disabled="!item.enabled" @click="topUpDialog = true" color="primary" x-large>
          {{ item.slug }}
        </v-btn>
      </div>
      <div class="d-flex justify-content-center w-100">
        <i>{{ $t('studies.setup.step6willStart') }}</i>
      </div>
    </div>

    <v-dialog max-width="600" v-model="topUpDialog">
      <TopUpRequestForm @sent="topUpDialog = false"/>
    </v-dialog>
  </div>
</template>

<script>
  import TopUpRequestForm from '~/components/study/finance/TopUpRequestForm'

  export default {
    name: 'TopUpCard',
    components: { TopUpRequestForm },
    props: {
      item: {
        type: Object,
        required: true
      }
    },
    data: () => ({
      topUpDialog: false
    })
  }
</script>

<style scoped>

</style>
