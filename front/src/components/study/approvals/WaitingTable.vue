<template>
  <v-card class="mb-4">
    <v-card-title>
      {{ $t('studies.approvals.paymentsWaiting') }}
    </v-card-title>
    <v-card-text>
      <v-data-table
        :footer-props="{
          'items-per-page-options': [10, 20, 50, -1]
        }"
        :headers="tableHeaders"
        :items="waitingList"
        :items-per-page="20"
      >
        <template v-slot:item.date="{ item }">
          {{ new Date(item.date).toLocaleDateString() }}
        </template>
        <template v-slot:item.visit_item_obj.study_item_obj.price="{ item }">
          {{ item.visit_item_obj.study_item_obj.price }}&nbsp;{{ $t('currencies.czk') }}
        </template>
        <template v-slot:item.id="{ item }">
          <div class="d-flex">
            <v-btn :title="$t('common.accept')" class="mr-1" color="primary" small @click="handleApproval({approved: true, id: item.id})">
              <v-icon>event_available</v-icon>
            </v-btn>
            <v-btn :title="$t('common.reject')" class="mr-1" color="red" dark small @click="handleOpenRejectDialog(item)">
              <v-icon>event_busy</v-icon>
            </v-btn>
            <v-btn v-if="item.can_be_deleted" :title="$t('common.resetVisit')" small @click="handleOpenResetDialog(item)">
              <img alt="" src="~/assets/img/cancel.png" style="height: 26px">
            </v-btn>
          </div>
        </template>
        <template v-slot:item.flagged="{ item }">
          <v-icon
            @click="handleOpenEditPatientDialog(item.patient_obj)"
            class="ml-2"
            color="yellow darken-2"
            v-if="item.flagged"
          >
            warning
          </v-icon>
        </template>
      </v-data-table>
      <AddReim @saved="$emit('changed')"/>
    </v-card-text>
    <v-dialog max-width="1080px" v-model="editPatientDialog">
      <PatientForm
        :title="editPatientDialogTitle"
        :update-mode="true"
        @close="handlePatientSaved"
        v-if="editPatientDialog"
      /><!-- the v-if is needed to call mounted method -->
    </v-dialog>
    <v-dialog max-width="400px" v-model="rejectDialog">
      <v-card>
        <v-card-title>{{ $t('studies.approvals.rejectReason') }}</v-card-title>
        <v-card-text>
          <v-textarea v-model="rejectReason" outlined/>
          <div class="d-flex justify-content-end">
            <v-btn class="mr-2" @click="rejectDialog = false">{{ $t('common.cancel') }}</v-btn>
            <v-btn
              :disabled="!rejectReason"
              @click="handleApproval({approved: false, id: rejectedItem.id, reject_reason: rejectReason})"
              color="primary"
            >
              {{ $t('common.reject') }}
            </v-btn>
          </div>
        </v-card-text>
      </v-card>
    </v-dialog>

    <v-dialog v-model="resetDialog" max-width="800px">
      <v-card>
        <v-card-title>{{ $t('common.resetVisit') }}</v-card-title>
        <v-card-text style="white-space: pre-line;">
          <p>
            {{ $t('studies.approvals.resetVisitInfo') }}
          </p>

          <v-data-table
            :headers="tableHeaders.slice(0, 5)"
            :items="resetVisitReims"
            disable-sort
          >
            <template v-slot:item.visit_item_obj.study_item_obj.price="{ item }">
              <span>{{ item.visit_item_obj.study_item_obj.price }}&nbsp;{{ $t('currencies.czk') }}</span>
            </template>
          </v-data-table>

          <div class="d-flex justify-content-end">
            <v-btn class="mr-2" @click="resetDialog = false">
              {{ $t('common.cancel') }}
            </v-btn>
            <v-btn color="primary" @click="handleResetVisit">
              {{ $t('common.resetVisit') }}
            </v-btn>
          </div>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script>
  import { mapActions, mapGetters, mapMutations, mapState } from 'vuex';

  import AddReim from '~/components/study/approvals/AddReim'
  import PatientForm from '~/components/study/patients/PatientForm'

  export default {
    name: 'ReimWaitingTable',
    components: { AddReim, PatientForm },
    computed: {
      ...mapGetters({
        waitingList: 'patientvisititems/waitingList'
      }),
      ...mapState({
        patient: state => state.patients.patient
      }),
      tableHeaders() {
        return [
          { value: 'patient_obj.site_obj.title', text: this.$t('common.siteNr') },
          { value: 'patient_obj.number', text: this.$t('common.patientNr') },
          { value: 'visit_item_obj.visit_obj.title', text: this.$t('common.visitNr') },
          { value: 'date', text: this.$t('common.date') },
          { value: 'visit_item_obj.study_item_obj.price', text: this.$t('common.reim') },
          { value: 'visit_item_obj.study_item_obj.title', text: this.$t('common.title') },
          { value: 'id', text: this.$t('common.action') },
          { value: 'flagged', text: this.$t('common.notice') },
          { value: 'status', text: this.$t('common.status') },
          { value: 'origin', text: this.$t('common.origin') },
        ]
      }
    },
    data() {
      return {
        addingSite: false,

        editPatientDialog: false,
        editPatientDialogTitle: '',
        editedPatientSiteId: null,

        rejectDialog: false,
        rejectedItem: null,
        rejectReason: '',

        resetDialog: false,
        resetVisitReims: [],
        resetVisit: null,

        selected: [],
      }
    },
    methods: {
      ...mapActions({
        deletePatientVisit: 'patientvisits/deletePatientVisit',
        getPatientVisitItemList: 'patientvisititems/getPatientVisitItemList',
        patchApproval: 'patientvisititems/patchApproval',
        returnReimsForPatientVisit: 'patientvisititems/returnReimsForPatientVisit',
      }),
      ...mapMutations({
        clearPatient: 'patients/clearPatient',
        setPatient: 'patients/setPatient'
      }),
      handleApproval(patchData) {
        this.patchApproval(patchData)
          .then(() => {
            this.$toast.success(this.$t('common.savedSuccessfully'))
            this.$emit('changed')
            this.resetToInitials()
          })
          .catch(e => this.$toast.error(e.message))
      },
      handleOpenEditPatientDialog(patient) {
        this.setPatient(patient)
        this.editPatientDialogTitle = `${this.$t('common.edit')} ${this.$t('common.patient')} ${patient.number}`
        this.editPatientDialog = true
      },
      handleOpenRejectDialog(item) {
        this.rejectedItem = item
        this.rejectDialog = true
      },
      async handleOpenResetDialog(item) {
        this.resetVisit = item
        this.resetDialog = true
        // this.resetVisitReims = await this.returnReimsForPatientVisit(item.patient_visit).results
        const resetVisitReimsResponse = await this.returnReimsForPatientVisit(item.patient_visit)
        this.resetVisitReims = resetVisitReimsResponse.results
      },
      handlePatientSaved() {
        this.getPatientVisitItemList()
        this.clearPatient()
        this.editPatientDialog = false
        this.$toast.success(this.$t('common.savedSuccessfully'))
      },
      async handleResetVisit() {
        try {
          await this.deletePatientVisit(this.resetVisit.patient_visit)
          this.resetDialog = false
          this.getPatientVisitItemList()
          this.$toast.success(this.$t('common.savedSuccessfully'))
        } catch (e) {
          this.$toast.error(e.message)
        }
      },
      resetToInitials() {
        this.rejectDialog = false
        this.rejectedItem = null
        this.rejectReason = ''
      }
    }
  }
</script>


