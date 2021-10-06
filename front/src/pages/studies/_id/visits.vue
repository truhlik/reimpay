<template>
  <div>
    <PageTitle :heading="title" :icon=icon :subheading=subheading class="mb-0" show-study-info/>

    <StudyMenu :isNew="false" :studyId="$route.params.id" active-item="visits"/>

    <v-row>
      <v-col cols="12" sm="9">
        <ArmSelector/>
      </v-col>
      <v-col cols="12" sm="3">
        <RegularVisitCosts/>
      </v-col>
    </v-row>

    <VisitCardRows/>

    <DoneButtonRow/>
  </div>
</template>

<script>
  import PageTitle from '~/components/partials/PageTitle'
  import DoneButtonRow from '~/components/study/DoneButtonRow';
  import StudyMenu from '~/components/study/StudyMenu'
  import ArmSelector from '~/components/study/visits/ArmSelector'
  import RegularVisitCosts from '~/components/study/visits/RegularVisitCosts'
  import VisitCardRows from '~/components/study/visits/VisitCardRows'

  export default {
    name: 'visits',
    components: { PageTitle, DoneButtonRow, StudyMenu, ArmSelector, RegularVisitCosts, VisitCardRows },
    async fetch({store, params}) {
      await store.dispatch('studies/getStudy', params.id)
      await store.dispatch('arms/getArmList')
    },
    data() {
      return {
        title: this.$t('studies.visits.title'),
        subheading: this.$t('studies.visits.subtitle'),
        icon: 'pe-7s-note2 icon-gradient bg-reimpay',
      }
    }
  }
</script>

<style scoped>

</style>
