<template>
  <v-card class="mb-4">
    <v-card-title>
      {{ $t('studies.finance.creditAccountBalance') }}
      <v-spacer/>
      <DateWidget
        :label="$t('common.exportFrom')"
        :value="exportFrom"
        @change="exportFrom = $event"
        reference="exportFrom"
      />
      <v-spacer/>
      <DateWidget
        :label="$t('common.exportTo')"
        :value="exportTo"
        @change="exportTo = $event"
        reference="exportTo"
      />
      <v-spacer/>
      <v-btn @click="handleExport" color="green darken-3" dark>
        <v-icon>table_chart</v-icon>&nbsp;{{ $t('common.export') }}
      </v-btn>
    </v-card-title>

    <v-card-text>
      <v-data-table
        :footer-props="{
          'items-per-page-options': [10, 20, 50, -1]
        }"
        :headers="tableHeaders"
        :items="creditList"
        :items-per-page="20"
      >
        <template v-slot:item.created_at="{ item }">
          {{ new Date(item.created_at).toLocaleDateString() }}
        </template>
      </v-data-table>
    </v-card-text>
  </v-card>
</template>

<script>
  import { mapActions, mapState } from 'vuex'
  import DateWidget from '~/components/partials/DateWidget'

  export default {
    name: 'CreditBalanceTable',
    components: { DateWidget },
    computed: {
      ...mapState({
        creditList: state => state.finance.creditList
      }),
      tableHeaders() {
        return [
          { value: 'created_at', text: this.$t('common.date') },
          { value: 'balance_amount', text: this.$t('common.amount') },
          { value: 'balance_type', text: this.$t('common.type') },
          // { value: 'vs', text: this.$t('common.vs') }
        ]
      }
    },
    data: () => ({
      exportFrom: '',
      exportTo: new Date().toISOString().substring(0, 10)
    }),
    methods: {
      ...mapActions({
        getCreditList: 'finance/getCreditList',
        getCreditListExport: 'finance/getCreditListExport'
      }),
      async handleExport() {
        try {
          await this.getCreditListExport({createdAtDateGte: this.exportFrom, createdAtDateLte: this.exportTo})
        } catch (e) {
          this.$toast.error(e.message)
        }
      }
    },
    created() {
      this.getCreditList()
    }
  }
</script>

<style scoped>

</style>
