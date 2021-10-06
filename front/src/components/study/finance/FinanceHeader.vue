<template>
  <v-card class="mb-4">
    <v-card-text>
      <v-row class="justify-content-between">
        <v-col class="d-flex align-items-center" cols="12" sm="8">
          <span class="d-inline-block mr-5">{{ $t('studies.finance.actualBalance') }}</span>
          <strong class="large">{{ parseInt(creditInfo.actual_balance).toLocaleString() }} {{ $t('currencies.czk') }}</strong>
        </v-col>
        <v-col class="text-right" cols="12" sm="4">
          <v-btn
            @click="topUpDialog = true"
            color="primary"
            x-large
          >
            {{ $t('studies.finance.topUp') }}
          </v-btn>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <span>{{ $t('common.paid') }}</span><br/>
          <strong>{{ parseInt(creditInfo.paid).toLocaleString() }} {{ $t('currencies.czk') }}</strong>
        </v-col>
        <v-col>
          <span>{{ $t('studies.finance.calculatedVisitsRemaining') }}</span><br/>
          <strong>{{ creditInfo.remaining_visits }}</strong>
        </v-col>
        <v-col>
          <span>{{ $t('studies.finance.averageVisitValue') }}</span><br/>
          <strong>{{ parseInt(creditInfo.avg_visit_value).toLocaleString() }} {{ $t('currencies.czk') }}</strong>
        </v-col>
        <v-col>
          <span>{{ $t('studies.finance.expectedBudgetNeeded') }}</span><br/>
          <strong>{{ parseInt(creditInfo.exp_budget_need).toLocaleString() }} {{ $t('currencies.czk') }}</strong>
        </v-col>
      </v-row>
    </v-card-text>

    <v-dialog max-width="600" v-model="topUpDialog">
      <TopUpRequestForm @sent="handleTopUpSent"/>
    </v-dialog>
  </v-card>
</template>

<script>
  import { mapActions, mapState } from 'vuex'
  import TopUpRequestForm from '~/components/study/finance/TopUpRequestForm'

  export default {
    name: 'FinanceHeader',
    components: { TopUpRequestForm },
    computed: {
      ...mapState({
        creditInfo: state => state.finance.creditInfo
      }),
    },
    data: () => ({
      topUpDialog: false
    }),
    methods: {
      ...mapActions({
        getCreditInfo: 'finance/getCreditInfo',
        getTopUpList: 'topups/getTopUpList'
      }),
      handleTopUpSent() {
        this.topUpDialog = false
        this.getTopUpList()
      }
    },
    created() {
      this.getCreditInfo()
    }
  }
</script>

<style lang="scss" scoped>
 strong {
   font-size: 1.4em;

   &.large {
     font-size: 2em;
   }
 }
</style>
