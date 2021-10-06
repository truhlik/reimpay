<template>
  <div v-if="patientDetail.patient_visit_items.length">
    <h3>{{ $t('patientDetail.paymentsHistory') }}</h3>
    <v-card>
      <v-card-text>
        <v-data-table
          :headers="tableHeaders"
          :items="patientDetail.patient_visit_items"
          :items-per-page="-1"
        >
          <template v-slot:item.date="{ item }">
            {{ new Date(item.date).toLocaleDateString() }}
          </template>
          <template v-slot:item.amount="{ item }">
            {{ item.amount }}&nbsp;{{ $t('currencies.czk') }}
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
  import { mapState } from 'vuex'

  export default {
    name: 'VisitApproval',
    computed: {
      ...mapState({
        patientDetail: state => state.patients.patientDetail
      }),
      tableHeaders() {
        return [
          {value: 'payment', text: this.$t('common.paymentNr')},
          {value: 'visit', text: this.$t('common.visitNr')},
          {value: 'date', text: this.$t('common.date')},
          {value: 'amount', text: this.$t('common.amount')},
          {value: 'payment_status', text: this.$t('common.paymentStatus')},
          {value: 'reject_reason', text: this.$t('common.note')},
        ]
      }
    },
  }
</script>
