<template>
  <div>
    <PageTitle :heading="title" :icon=icon :subheading=subheading class="mb-0" show-study-info/>

    <StudyMenu :isNew="false" :studyId="$route.params.id" active-item="sites"/>

    <SiteList/>

    <DoneButtonRow/>
  </div>
</template>

<script>
  import PageTitle from '~/components/partials/PageTitle';
  import DoneButtonRow from '~/components/study/DoneButtonRow';
  import StudyMenu from '~/components/study/StudyMenu';
  import SiteList from '~/components/study/sites/SiteList';

  export default {
    name: "sites",
    components: { PageTitle, StudyMenu, SiteList, DoneButtonRow },
    async fetch({store, params}) {
      await store.dispatch('studies/getStudy', params.id)
    },
    data() {
      return {
        title: this.$t('studies.sites.title'),
        subheading: this.$t('studies.sites.subtitle'),
        icon: 'pe-7s-note2 icon-gradient bg-reimpay',
      }
    },
  }
</script>

<style scoped>

</style>
