<template>
  <div>
    <PageTitle :heading="title" :icon=icon :subheading=subheading class="mb-0"/>

    <StudyMenu active-item="setup" :isNew="true" class="mb-10"/>

    <SetupWizard/>
  </div>
</template>

<script>
  import { mapMutations } from 'vuex'
  import PageTitle from '~/components/partials/PageTitle'
  import StudyMenu from '~/components/study/StudyMenu'
  import SetupWizard from '~/components/study/setup/SetupWizard'

  export default {
    name: 'setup',
    components: { StudyMenu, PageTitle, SetupWizard },
    data() {
      return {
        title: this.$t('studies.setup.title'),
        subheading: this.$t('studies.setup.subtitle'),
        icon: 'pe-7s-note2 icon-gradient bg-reimpay',
      }
    },
    methods: {
      ...mapMutations({
        clearStudy: 'studies/clearStudy'
      }),
    },
    created() {
      this.clearStudy();
    }
  }
</script>

