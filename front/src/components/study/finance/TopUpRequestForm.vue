<template>
  <v-card>
    <v-card-title>{{ $t('studies.finance.newTopUpRequest') }}</v-card-title>
    <v-card-text>
      <v-row>
        <FormInput
          :breakpoints="{ xs: 12, sm: 12, md: 12, lg: 8 }"
          :label="$t('common.amount')"
          :rules="[
            value => !isNaN(value) && value >= 1000 || $t('errors.atLeast1000')
          ]"
          :value="topUpAmount"
          @input="topUpAmount = parseInt($event.value)"
          field="amount"
          type="number"
        />
        <v-btn
          :disabled="!topUpAmount  || topUpAmount < 1000"
          @click="handleGenerateRequest"
          color="primary"
        >
          {{ $t('studies.finance.generateRequest') }}
        </v-btn>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>
  import { mapActions, mapState } from 'vuex'
  import FormInput from '~/components/partials/FormInput'
  import downloadFile from '~/helpers/downloadFile'

  export default {
    name: 'TopUpRequestForm',
    components: { FormInput },
    computed: {
      ...mapState({
        topUp: state => state.topups.topUp
      })
    },
    data: () => ({
      topUpAmount: null
    }),
    methods: {
      ...mapActions({
        createTopUp: 'topups/createTopUp'
      }),
      async handleGenerateRequest() {
        try {
          await this.createTopUp(this.topUpAmount)
          this.$emit('sent')
          downloadFile(this.$axios, this.$toast, this.topUp.file, 'TopupRequest.pdf')
          this.$toast.success(this.$t('common.sentSuccessfully'))
        } catch (e) {
          this.$toast.error(e.message)
        }
      }
    },
  }
</script>

<style scoped>

</style>
