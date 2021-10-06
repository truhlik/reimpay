<template>
  <div>
    <PageTitle :heading="title" :icon=icon :subheading=subheading class="mb-0" show-study-info/>

    <StudyMenu :isNew="false" :studyId="$route.params.id" active-item="reims"/>

    <SetupItems/>

    <DoneButtonRow/>
  </div>
</template>

<script>
  import PageTitle from '~/components/partials/PageTitle'
  import DoneButtonRow from '~/components/study/DoneButtonRow'
  import StudyMenu from '~/components/study/StudyMenu'
  import SetupItems from '~/components/study/reims/SetupItems'


  export default {
    name: 'items',
    components: {PageTitle, StudyMenu, SetupItems, DoneButtonRow },
    async fetch({store, params}) {
      await store.dispatch('studies/getStudy', params.id);
    },
    data() {
      return {
        title: this.$t('studies.reims.title'),
        subheading: this.$t('studies.reims.subtitle'),
        icon: 'pe-7s-note2 icon-gradient bg-reimpay',
      }
    },
  }
</script>
