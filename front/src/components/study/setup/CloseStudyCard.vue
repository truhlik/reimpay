<template>
  <div class="color-secondary d-flex align-items-center justify-content-between w-100">
    <span class="font-size-lg">{{ item.label }}</span>
    <v-spacer/>
    <span class="d-inline-flex justify-content-end" style="max-width: 120px">
      <v-btn
        color="primary"
        :disabled="!item.enabled"
        v-if="!item.completed"
        @click="handleOpenDialog"
      >
        {{ item.slug }}
      </v-btn>
      <v-icon color="green" v-else>check</v-icon>
    </span>
    <v-dialog max-width="600" v-model="closeStudyDialog">
      <v-card>
        <v-card-title>
          {{ $t('studies.setup.step10CloseDialogTitle') }}
        </v-card-title>
        <v-card-text>
          <p>{{ $t('studies.setup.step10ReallyClose') }}</p>

          <p v-if="activePatientCount">
            <strong class="color-yellow">
              {{ $t('studies.setup.step10ThereAre') }}
              {{ activePatientCount }}
              {{ $t('studies.setup.step10ActivePatients') }}
            </strong>
          </p>

          <p v-if="unapprovedItemsCount">
            <strong class="color-red">
              {{ $t('studies.setup.step10ThereAre') }}
              {{ unapprovedItemsCount }}
              {{ $t('studies.setup.step10UnapprovedReims') }}
            </strong>
          </p>
        </v-card-text>
        <v-card-actions>
          <v-spacer/>
          <v-btn color="gray" @click="closeStudyDialog = false">{{ $t('common.dismiss') }}</v-btn>
          <v-btn color="primary" :disabled="!!unapprovedItemsCount" @click="handleCloseStudy">
            {{ $t('common.closeStudy') }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
  import { mapActions, mapState } from 'vuex'

  export default {
    name: 'CloseStudyCard',
    props: {
      item: {
        type: Object,
        required: true
      }
    },
    computed: {
      ...mapState({
        activePatientCount: state => state.patients.activePatientCount,
        unapprovedItemsCount: state => state.patientvisititems.unapprovedItemsCount
      })
    },
    data: () => ({
      closeStudyDialog: false
    }),
    methods: {
      ...mapActions({
        getActivePatientCount: 'patients/getActivePatientCount',
        getUnapprovedItemsCount: 'patientvisititems/getUnapprovedItemsCount',
        patchStudy: 'studies/patchStudy'
      }),
      async handleCloseStudy() {
        try {
          await this.patchStudy({ status: 'BILLING' })
          this.closeStudyDialog = false
        } catch (e) {
          this.$toast.error(e.message)
        }
      },
      handleOpenDialog() {
        this.getActivePatientCount()
        this.getUnapprovedItemsCount()
        this.closeStudyDialog = true
      }
    }
  }
</script>

<style scoped>

</style>
