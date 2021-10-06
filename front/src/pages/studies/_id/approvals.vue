<template>
  <div>
    <PageTitle :heading="title" :icon=icon :subheading=subheading class="mb-0" show-study-info/>

    <StudyMenu :isNew="false" :studyId="$route.params.id" active-item="approvals"/>

    <FinanceHeader v-if="!isAdmin"/>

    <WaitingTable @changed="getPatientVisitItemList"/>

    <PatientsToEditTable/>

    <HistoryTable @changed="getPatientVisitItemList"/>

    <TopUpTable v-if="!isAdmin"/>
  </div>
</template>

<script>
  import { mapActions, mapGetters } from 'vuex'

  import PageTitle from '~/components/partials/PageTitle'
  import StudyMenu from '~/components/study/StudyMenu'

  import HistoryTable from '~/components/study/approvals/HistoryTable'
  import PatientsToEditTable from '~/components/study/approvals/PatientsToEditTable'
  import WaitingTable from '~/components/study/approvals/WaitingTable'

  import FinanceHeader from '~/components/study/finance/FinanceHeader'
  import TopUpTable from '~/components/study/finance/TopUpTable'

  export default {
    name: "approvals",
    components: { PageTitle, StudyMenu, WaitingTable, HistoryTable, FinanceHeader, PatientsToEditTable, TopUpTable },
    async fetch({ store, params }) {
      await store.dispatch('studies/getStudy', params.id)
    },
    computed: {
      ...mapGetters({
        isAdmin: 'account/isAdmin'
      })
    },
    data() {
      return {
        title: this.$t('studies.approvals.title'),
        subheading: this.$t('studies.approvals.subtitle'),
        icon: 'pe-7s-note2 icon-gradient bg-reimpay',
      }
    },
    methods: {
      ...mapActions({
        getPatientList: 'patients/getPatientList',
        getPatientVisitItemList: 'patientvisititems/getPatientVisitItemList',
        getSiteList: 'sites/getSiteList',
      }),
    },
    created() {
      this.getPatientVisitItemList()
      this.getSiteList()      // for add reim selects and history table filter
      this.getPatientList()   // for add reim selects and history table filter
    }
  }
</script>

<style scoped>

</style>
