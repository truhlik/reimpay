<template>
  <div>
    <PageTitle
      :heading="`${$t('common.patient')} ${patientDetail.number} ${$t('common.detail')}`"
      :subheading="`${$t('common.study')} ${patientDetail.study_obj.identifier} (${patientDetail.arm_name})`"
      icon="pe-7s-user icon-gradient bg-reimpay"
    />

    <VisitApproval/>

    <ReimHistory/>
  </div>
</template>

<script>
  import { mapState } from 'vuex'
  import PageTitle from '~/components/partials/PageTitle'
  import ReimHistory from '~/components/patient/ReimHistory'
  import VisitApproval from '~/components/patient/VisitApproval'

  export default {
    name: 'uid',
    auth: false,
    layout: 'simple',
    components: { PageTitle, ReimHistory, VisitApproval },
    async fetch({store, params}) {
      await store.dispatch('patients/getPatient', params.uid);
    },
    computed: {
      ...mapState({
        patientDetail: state => state.patients.patientDetail
      })
    }
  }
</script>

<style scoped>
  h6 {
    font-weight: 700;
  }
</style>
