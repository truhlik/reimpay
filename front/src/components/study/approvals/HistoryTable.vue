<template>
  <v-card class="mb-4">
    <v-card-title>
      {{ $t('studies.approvals.reimsHistory') }}
      <v-spacer/>
      <div class="d-flex align-items-center flex-column flex-lg-row flex-wrap">
        <FormAutocomplete
          clearable
          class="mb-2 mb-lg-0"
          dense
          hideDetails
          :label="$t('common.site')"
          :items="siteOptionList"
          style="max-width: 200px"
          :value="filterObject.patientVisitPatientSiteId"
          @change="filterObject.patientVisitPatientSiteId = $event.value"
        />
        <FormSelect
          clearable
          class="mb-2 mb-lg-0"
          dense
          hideDetails
          :label="$t('common.patient')"
          :items="patientOptionList"
          style="max-width: 200px"
          :value="filterObject.patientVisitPatientId"
          @change="filterObject.patientVisitPatientId = $event.value"
        />
        <FormSelect
          clearable
          class="mb-2 mb-lg-0"
          dense
          hideDetails
          :label="$t('common.approved')"
          :items="approvedOptions"
          style="max-width: 200px"
          :value="filterObject.approved"
          @change="filterObject.approved = $event.value"
        />
        <FormSelect
          clearable
          class="mb-2 mb-lg-0"
          dense
          hideDetails
          :label="$t('common.status')"
          :items="statusOptions"
          style="max-width: 200px"
          :value="filterObject.paymentStatus"
          @change="filterObject.paymentStatus = $event.value"
        />
      </div>
    </v-card-title>

    <v-card-text>
      <v-data-table
        disable-sort
        :footer-props="{
          'items-per-page-options': [10, 20, 50, -1]
        }"
        :headers="tableHeaders"
        :items="patientVisitItemHistoryList"
        :options="{
          itemsPerPage: patientVisitItemHistoryPagination.page_size,
          page: patientVisitItemHistoryPagination.page,
        }"
        :server-items-length="patientVisitItemHistoryPagination.count || 0"
        @update:items-per-page="handlePageSizeChanged"
        @update:page="handlePageChanged"
      >
        <template v-slot:item.date="{ item }">
          {{ new Date(item.date).toLocaleDateString() }}
        </template>
        <template v-slot:item.visit_item_obj.study_item_obj.price="{ item }">
          {{ item.visit_item_obj.study_item_obj.price }}&nbsp;{{ $t('currencies.czk') }}
        </template>
        <template v-slot:item.approved="{ item }">
          <v-icon color="green" v-if="item.approved">check</v-icon>
          <v-icon color="red" v-else>clear</v-icon>
        </template>
        <template v-slot:item.id="{ item }">
          <v-btn @click="handleApproval({approval: true, id: item.id})" color="primary" small text>
            {{ $t('common.accept') }}
          </v-btn>
          <v-btn color="red" small text>
            {{ $t('common.reject') }}
          </v-btn>
        </template>
      </v-data-table>
    </v-card-text>
  </v-card>
</template>

<script>
  import { mapActions, mapGetters, mapMutations, mapState } from 'vuex'
  import FormAutocomplete from '~/components/partials/FormAutocomplete'
  import FormSelect from '~/components/partials/FormSelect'

  export default {
    name: 'ReimHistoryTable',
    components: { FormAutocomplete, FormSelect },
    computed: {
      ...mapGetters({
        patientOptionList: 'patients/patientOptionList',
        siteOptionList: 'sites/siteOptionList',
      }),
      ...mapState({
        patientVisitItemHistoryList: state => state.patientvisititems.patientVisitItemHistoryList,
        patientVisitItemHistoryPagination: state => state.patientvisititems.patientVisitItemHistoryPagination
      }),
      approvedOptions() {
        return [
          { value: 'any', text: this.$t('common.any') },
          { value: 'true', text: this.$t('common.approved') },
          { value: 'false', text: this.$t('common.rejected') },
        ]
      },
      statusOptions() {
        return [
          { value: null, text: this.$t('common.any') },
          { value: 'WAITING', text: this.$t('common.waiting') },
          { value: 'SENT', text: this.$t('common.sent') },
        ]
      },
      tableHeaders() {
        return [
          { value: 'patient_obj.site_obj.title', text: this.$t('common.siteNr') },
          { value: 'patient_obj.number', text: this.$t('common.patientNr') },
          { value: 'visit_item_obj.visit_obj.title', text: this.$t('common.visitNr') },
          { value: 'date', text: this.$t('common.date') },
          { value: 'visit_item_obj.study_item_obj.price', text: this.$t('common.reim') },
          { value: 'visit_item_obj.study_item_obj.title', text: this.$t('common.title') },
          { value: 'approved', text: this.$t('common.approved') },
          { value: 'payment', text: this.$t('common.paymentNr') },
          { value: 'status', text: this.$t('common.status') }
        ]
      }
    },
    data() {
      return {
        addingSite: false,
        filterObject: {
          approved: 'any',
          paymentStatus: null,
          patientVisitPatientSiteId: null,
          patientVisitPatientId: null
        },
      }
    },
    methods: {
      ...mapActions({
        getPatientVisitItemHistoryList: 'patientvisititems/getPatientVisitItemHistoryList',
        patchApproval: 'patientvisititems/patchApproval'
      }),
      ...mapMutations({
        setPaginationPage: 'patientvisititems/setPatientVisitItemHistoryPaginationPage',
        setPaginationSize: 'patientvisititems/setPatientVisitItemHistoryPaginationSize'
      }),
      handleApproval(patchData) {
        this.patchApproval(patchData)
          .then(() => {
            this.$toast.success(this.$t('common.savedSuccessfully'))
            this.$emit('changed')
          })
          .catch(e => this.$toast.error(e.message))
      },
      handlePageChanged(pageNumber) {
        this.setPaginationPage(pageNumber)
        this.getPatientVisitItemHistoryList(this.filterObject)
      },
      handlePageSizeChanged(pageSize) {
        this.setPaginationSize(pageSize)
        this.getPatientVisitItemHistoryList(this.filterObject)
      },
      handleSiteSaved() {
        this.addingSite = false;
        this.getSiteList(this.$route.params.id);
      }
    },
    created() {
      this.getPatientVisitItemHistoryList(this.filterObject)
    },
    watch: {
      filterObject: {
        deep: true,
        handler: function () {
          this.getPatientVisitItemHistoryList(this.filterObject)
        }
      }
    }
  }
</script>


