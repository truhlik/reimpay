<template>

  <v-expansion-panels>
    <v-expansion-panel
      class="mb-2"
      :key="site.id"
      v-for="site in sitePatientList"
    >
      <v-expansion-panel-header class="font-size-lg d-flex flex-wrap panel-heading py-0" hide-actions>
        <v-row align="center">
          <v-col sm="6" md="3"><strong>{{ site.title }}</strong></v-col>
          <v-col sm="6" md="3">{{ $t('common.expected') }}: {{ site.expected_patients }}</v-col>
          <v-col sm="6" md="2">{{ $t('common.actual') }}: {{ site.patients.length }}</v-col>
          <v-col sm="6" md="4">
            <v-btn @click.stop="$emit('btnClick', site.id)" class="mr-1" color="primary" small :title="$t('studies.patients.addPatient') ">
              <v-icon small>add</v-icon>
            </v-btn>
            <v-btn
              :title="$t('studies.sites.downloadInfo')" class="px-2" color="blue darken-2" dark small
              @click.prevent="downloadFile($axios, $toast, site.site_instructions_path, 'Instructions.pdf')"
            >
              <v-icon small>event_note</v-icon>
            </v-btn>
            <v-btn
              :title="$t('studies.sites.downloadAgreement')" class="px-2" color="blue darken-2" dark small
              @click.prevent="downloadFile($axios, $toast, site.contract_path, 'PatientForm.pdf')"
            >
              <v-icon small>event_available</v-icon>
            </v-btn>
          </v-col>
        </v-row>
      </v-expansion-panel-header>
      <v-expansion-panel-content>
        <v-data-table
          :headers="tableHeaders"
          :items="site.patients"
        >
        </v-data-table>
      </v-expansion-panel-content>
    </v-expansion-panel>
  </v-expansion-panels>
</template>

<script>
  import { mapActions, mapState } from 'vuex'
  import downloadFile from '~/helpers/downloadFile'

  export default {
    name: 'SitePatientTables',
    computed: {
      ...mapState({
        sitePatientList: state => state.sites.sitePatientList
      }),
      tableHeaders() {
        return [
          {value: 'number', text: this.$t('common.patientNr')},
          {value: 'arm_name', text: this.$t('common.arm')},
          {value: 'payment_type', text: this.$t('studies.patients.paymentType')},
          {value: 'status', text: this.$t('common.status')},
          {value: 'visits', text: this.$t('common.visits')},
          {value: 'paid', text: this.$t('common.paid')},
          // {value: 'id', text: ''}
        ]
      }
    },
    methods: {
      ...mapActions({
        getSitePatientList: 'sites/getSitePatientList'
      }),
      downloadFile: downloadFile
    },
    created() {
      this.getSitePatientList();
    }
  }
</script>

