<template>
  <div>
    <PageTitle :heading="title" :icon=icon :subheading=subheading class="mb-0" show-study-info/>

    <StudyMenu :isNew="false" :studyId="$route.params.id" active-item="general"/>

    <SetupInfo/>

    <SetupPayment/>

    <v-row class="mb-5">
      <v-col class="text-center">
        <v-btn @click="handleUpdateStudy" color="primary" x-large>
          {{ $t('common.save') }}
        </v-btn>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import {mapActions, mapMutations} from 'vuex'
  import PageTitle from '~/components/partials/PageTitle'
  import StudyMenu from '~/components/study/StudyMenu'

  import SetupInfo from '~/components/study/general/SetupInfo'
  import SetupPayment from '~/components/study/general/SetupPayment'

  export default {
    name: 'general',
    components: { StudyMenu, PageTitle, SetupInfo, SetupPayment },
    async fetch({store, params}) {
      await store.dispatch('studies/getStudy', params.id)
    },
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
        updateStudy: 'studies/updateStudy'
      }),
      ...mapMutations({
        clearErrorObject: 'errors/clearErrorObject'
      }),
      async handleUpdateStudy() {
        try {
          await this.updateStudy()
          this.clearErrorObject()
          this.$toast.success(this.$t('common.savedSuccessfully'))
          this.$router.push(this.localePath({ name: 'studies-id-setup', params: this.$route.params.id }))
        } catch (e) {
          this.$toast.error(e.message)
        }
      }
    },
    mounted() {
      this.$store.dispatch('company/getUserList')
    }
  }
</script>
