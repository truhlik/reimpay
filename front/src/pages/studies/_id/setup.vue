<template>
  <div>
    <PageTitle :heading="title" :icon=icon :subheading=subheading class="mb-0" show-study-info/>

    <StudyMenu :isNew="false" :studyId="$route.params.id" active-item="setup" class="mb-10"/>

    <SetupWizard/>
  </div>
</template>

<script>
  import PageTitle from '~/components/partials/PageTitle';
  import StudyMenu from '~/components/study/StudyMenu';
  import SetupWizard from '~/components/study/setup/SetupWizard';

  export default {
    name: 'setup',
    components: { PageTitle, StudyMenu, SetupWizard},
    async fetch({store, params}) {
      await store.dispatch('studies/getStudy', params.id);
    },
    data() {
      return {
        title: this.$t('studies.setup.title'),
        subheading: this.$t('studies.setup.subtitle'),
        icon: 'pe-7s-note2 icon-gradient bg-reimpay',
      }
    },
  }
</script>

