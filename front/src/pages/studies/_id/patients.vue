<template>
  <div>
    <PageTitle :heading=title :icon=icon :subheading=subheading show-study-info/>

    <StudyMenu :isNew="false" :studyId="$route.params.id" active-item="patients"/>

    <!--    TODO site filter-->

    <v-dialog max-width="1080px" v-model="addingPatient">
      <PatientForm :siteId="siteId" @close="addingPatient = false" v-if="addingPatient"/>
      <!-- the v-if is needed to call mounted method -->
    </v-dialog>

    <SitePatientTables @btnClick="handleOpenPatientDialog($event)"/>
  </div>
</template>

<script>
  import { mapActions } from 'vuex'

  import PageTitle from '~/components/partials/PageTitle'
  import StudyMenu from '~/components/study/StudyMenu'
  import PatientForm from '~/components/study/patients/PatientForm'
  import SitePatientTables from '~/components/study/patients/SitePatientTables'

  export default {
    name: 'patients',
    components: { PageTitle, StudyMenu, PatientForm, SitePatientTables },
    async fetch({store, params}) {
      await store.dispatch('studies/getStudy', params.id);
    },
    data() {
      return {
        title: this.$t('studies.patients.title'),
        subheading: this.$t('studies.patients.subtitle'),
        icon: 'pe-7s-note2 icon-gradient bg-reimpay',

        addingPatient: false,
        siteId: null
      }
    },
    methods: {
      ...mapActions({
        getSiteList: 'sites/getSiteList'
      }),
      handleOpenPatientDialog(siteId) {
        this.siteId = parseInt(siteId)
        this.addingPatient = true
      }
    },
    created() {
      this.getSiteList()
    }
  }
</script>

<style scoped>

</style>
