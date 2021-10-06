<template>
  <v-card>
    <v-card-text>
      <v-data-table
        :footer-props="{
          'items-per-page-options': [20, 50, 100, -1]
        }"
        :headers="tableHeaders"
        :items="invoiceList"
      >
        <template v-slot:item.invoice_number="{ item }">
          <a :href="item.fakturoid_public_url" target="_blank">
            {{ item.invoice_number }}
          </a>
        </template>
        <template v-slot:item.issue_date="{ item }">
          {{ new Date(item.issue_date).toLocaleDateString() }}
        </template>
        <template v-slot:item.amount="{ item }">
          {{ item.amount }}&nbsp;{{ $t('currencies.czk') }}
        </template>
      </v-data-table>
    </v-card-text>
  </v-card>
</template>

<script>
  import { mapActions, mapState } from 'vuex'

  export default {
    name: 'InvoiceTable',
    computed: {
      ...mapState({
        invoiceList: state => state.invoices.invoiceList,
      }),
      tableHeaders() {
        return [
          {value: 'invoice_number', text: this.$t('invoices.number')},
          {value: 'issue_date', text: this.$t('invoices.dateOfIssue')},
          {value: 'amount', text: this.$t('common.amount')},
          {value: 'status', text: this.$t('common.status')}
        ]
      }
    },
    methods: {
      ...mapActions({
        getInvoiceList: 'invoices/getInvoiceList'
      })
    },
    created() {
      this.getInvoiceList()
    }
  }
</script>

<style scoped>

</style>
