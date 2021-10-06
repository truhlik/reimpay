<template>
  <div>
    <PageTitle :heading=title :icon=icon :subheading=subheading show-study-info/>

    <StudyMenu :isNew="false" :studyId="$route.params.id" active-item="finance"/>

    <FinanceHeader/>

    <TopUpTable/>

    <HistoryTable @changed="getPatientVisitItemList"/>

    <CreditBalanceTable/>
  </div>
</template>

<script>
  import { mapActions } from 'vuex'
  import PageTitle from '~/components/partials/PageTitle'
  import StudyMenu from '~/components/study/StudyMenu'

  import CreditBalanceTable from '~/components/study/finance/CreditBalanceTable'
  import FinanceHeader from '~/components/study/finance/FinanceHeader'
  import HistoryTable from '~/components/study/approvals/HistoryTable'
  import TopUpTable from '~/components/study/finance/TopUpTable'

  export default {
    name: 'finance',
    components: { PageTitle, StudyMenu, FinanceHeader, TopUpTable, HistoryTable, CreditBalanceTable },
    async fetch({store, params}) {
      await store.dispatch('studies/getStudy', params.id);
    },
    data() {
      return {
        title: this.$t('studies.finance.title'),
        subheading: this.$t('studies.finance.subtitle'),
        icon: 'pe-7s-cash icon-gradient bg-reimpay',
      }
    },
    methods: {
      ...mapActions({
        getPatientVisitItemList: 'patientvisititems/getPatientVisitItemList',
      })
    },
    created() {
      this.getPatientVisitItemList()
    }
  }
</script>
