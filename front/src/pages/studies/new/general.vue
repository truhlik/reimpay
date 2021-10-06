<template>
  <div>
    <PageTitle :heading="title" :icon=icon :subheading=subheading class="mb-0"/>

    <StudyMenu :isNew="true" active-item="general"/>

    <SetupInfo/>

    <SetupPayment/>

    <v-row class="mb-5">
      <v-col class="text-center">
        <v-btn @click="handleCreateStudy" color="primary" x-large>
          {{ $t('common.save') }}
        </v-btn>
      </v-col>
    </v-row>
  </div>
</template>

<script>
  import { mapActions, mapMutations } from 'vuex'

  import PageTitle from '~/components/partials/PageTitle'
  import StudyMenu from '~/components/study/StudyMenu'

  import SetupInfo from '~/components/study/general/SetupInfo'
  import SetupPayment from '~/components/study/general/SetupPayment'

  export default {
    name: 'general',
    components: { StudyMenu, PageTitle, SetupInfo, SetupPayment },
    computed: {
    },
    data() {
      return {
        title: this.$t('studies.general.title'),
        subheading: this.$t('studies.general.subtitle'),
        icon: 'pe-7s-note2 icon-gradient bg-reimpay',
      }
    },
    methods: {
      ...mapActions({
        createStudy: 'studies/createStudy',
        getStudyList: 'studies/getStudyList'
      }),
      ...mapMutations({
        clearStudy: 'studies/clearStudy',
        clearErrorObject: 'errors/clearErrorObject'
      }),
      handleCreateStudy() {
        this.createStudy().then(
          () => {
            this.$toast.success(this.$t('common.savedSuccessfully'))
            this.clearErrorObject()
            this.$router.push(
              this.localePath({name: 'studies-id-setup', params: {id: this.$store.state.studies.study.id}})
            )
            this.getStudyList()
          },
          e => this.$toast.error(e.message)
        )
      }
    },
    created() {
      this.clearStudy()
    }
  }
</script>

