<template>
  <v-card class="mb-4" v-if="patientsToEditList.length">
    <v-card-title>
      {{ $t('studies.approvals.patientsToEdit') }}
    </v-card-title>

    <v-card-text>
      <v-data-table
        :headers="tableHeaders"
        :items="patientsToEditList"
      >
        <template v-slot:item.id="{ item }">
          <v-btn @click="handleEditPatient(item)" color="primary" small>
            <v-icon v-text="'edit'"/>
          </v-btn>
        </template>
      </v-data-table>
    </v-card-text>
    <v-dialog max-width="1080px" v-model="editPatientDialog">
      <PatientForm
        :title="editPatientDialogTitle"
        :update-mode="true"
        @close="handlePatientSaved"
        v-if="editPatientDialog && patient"/><!-- the v-if is needed to call mounted method -->
    </v-dialog>
  </v-card>
  <div v-else />
</template>

<script>
import {mapActions, mapMutations, mapState} from 'vuex'
  import FormAutocomplete from '~/components/partials/FormAutocomplete'
  import FormSelect from '~/components/partials/FormSelect'
  import PatientForm from '~/components/study/patients/PatientForm'

  export default {
    name: 'SiteList',
    components: { FormAutocomplete, FormSelect, PatientForm },
    computed: {
      ...mapState({
        patient: state => state.patients.patient,
        patientsToEditList: state => state.patients.toEditList
      }),
      tableHeaders() {
        return [
          { value: 'number', text: this.$t('common.patientNr') },
          { value: 'arm_name', text: this.$t('common.arm') },
          { value: 'payment_type', text: this.$t('studies.patients.paymentType') },
          { value: 'status', text: this.$t('common.status') },
          { value: 'visits', text: this.$t('common.visits') },
          { value: 'paid', text: this.$t('common.paid') },
          { value: 'id', text: '' }
        ]
      }
    },
    data() {
      return {
        editPatientDialog: false,
        editPatientDialogTitle: ''
      }
    },
    methods: {
      ...mapActions({
        getPatientToEditList: 'patients/getToEditList'
      }),
      ...mapMutations({
        clearPatient: 'patients/clearPatient',
        setPatient: 'patients/setPatient'
      }),
      handleEditPatient(patient) {
        this.setPatient(patient)
        this.editPatientDialogTitle = `${this.$t('common.edit')} ${this.$t('common.patient')} ${patient.number}`  // Číslo se smaže kvůli potvrzení editace, musím proto poslat string
        this.editPatientDialog = true
      },
      handlePatientSaved() {
        this.editPatientDialog = false
        this.getPatientToEditList()
      }
    },
    created() {
      this.getPatientToEditList()
    },
    destroyed() {
      this.clearPatient()
    }
  }
</script>


