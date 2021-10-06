<template>
 <div>
    <v-btn @click="addReimDialog = true" color="primary" text>
      +{{ $t('studies.visits.addReim') }}
    </v-btn>
    <v-dialog max-width="320px" v-model="addReimDialog">
      <v-card>
        <v-card-title>
          {{ $t('studies.visits.addReim') }}
        </v-card-title>
        <v-card-text>
          <FormAutocomplete
            :breakpoints="{sm: 12, md: 12, lg: 12, xl: 12}"
            dense
            :items="siteOptionList"
            :label="$t('common.site')"
            :value="selectedSiteId"
            @change="handleSiteSelected($event.value)"
          />
          <FormAutocomplete
            :breakpoints="{sm: 12, md: 12, lg: 12, xl: 12}"
            dense
            :items="patientOptionList"
            :label="$t('common.patient')"
            :readonly="!selectedSiteId"
            :value="selectedPatientId"
            @change="handlePatientSelected($event.value)"
          />
          <FormAutocomplete
            :breakpoints="{sm: 12, md: 12, lg: 12, xl: 12}"
            @change="handlePatientVisitSelected($event.value)"
            :items="patientVisitOptionList"
            :label="$t('common.patientVisit')"
            :readonly="!selectedPatientId"
            :value="selectedPatientVisitObj"
            dense
          />
          <FormAutocomplete
            :breakpoints="{sm: 12, md: 12, lg: 12, xl: 12}"
            :items="visitItemOptionList"
            :value="selectedVisitItemId"
            :label="$t('common.reim')"
            :readonly="!selectedPatientVisitObj"
            @change="handleVisitItemSelected($event.value)"
            dense
          />
          <div class="text-right">
            <v-btn @click="handleCreateReim" color="primary">
              {{ $t('common.add') }}
            </v-btn>
          </div>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
  import { mapActions, mapGetters } from 'vuex'
  import FormAutocomplete from '~/components/partials/FormAutocomplete'

  export default {
    name: 'AddReim',
    components: { FormAutocomplete },
    computed: {
      ...mapGetters({
        siteOptionList: 'sites/siteOptionList',
        patientOptionList: 'patients/patientOptionList',
        patientVisitOptionList: 'patientvisits/patientVisitOptionList',
        visitItemOptionList: 'visititems/visitItemOptionList',
      })
    },
    data: () => ({
      addReimDialog: false,
      selectedPatientId: null,
      selectedPatientVisitObj: null,
      selectedVisitItemId: null,
      selectedSiteId: null
    }),
    methods: {
      ...mapActions({
        createPatientVisitItem: 'patientvisititems/createPatientVisitItem',
        getPatientList: 'patients/getPatientList',
        getPatientVisitList: 'patientvisits/getPatientVisitList',
        getVisitItemList: 'visititems/getVisitItemList',
      }),
      handleCreateReim() {
        this.createPatientVisitItem({
          approved: null,
          patient_visit: this.selectedPatientVisitObj.id,
          visit_item: this.selectedVisitItemId
        }).then(() => {
          this.$toast.success(this.$t('common.savedSuccessfully'))
          this.resetToInitial()
          this.$emit('saved')
        }).catch((e) => this.$toast.error(e.message))
      },
      handlePatientSelected(patientId) {
        this.selectedPatientId = patientId

        this.selectedPatientVisitObj = null
        this.selectedVisitItemId = null

        this.getPatientVisitList(patientId)
      },
      handlePatientVisitSelected(patientVisit) {
        this.selectedPatientVisitObj = patientVisit
        this.selectedVisitItemId = null

        this.getVisitItemList(patientVisit.visit)
      },
      handleSiteSelected(siteId) {
        this.selectedSiteId = siteId

        this.selectedPatientId = null
        this.selectedPatientVisitObj = null
        this.selectedVisitItemId = null

        this.getPatientList(siteId)
      },
      handleVisitItemSelected(visitItemId) {
        this.selectedVisitItemId = visitItemId
      },
      resetToInitial() {
        this.addReimDialog = false
        this.selectedSiteId = null
        this.selectedPatientId = null
        this.selectedPatientVisitObj = null
        this.selectedVisitItemId = null
      },
    },
    mounted() {
      // this.getSiteList() loaded in approvals.vue
    }
  }
</script>

<style scoped>

</style>
