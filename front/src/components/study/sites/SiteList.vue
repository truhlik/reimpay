<template>
  <v-card class="mb-4">
<!--    <v-card-title>-->
<!--      {{ $t('menu.sites') }}-->
<!--    </v-card-title>-->
    <v-card-text>
      <v-data-table
        :headers="tableHeaders"
        :items="siteList"
        show-select
      >
        <template v-slot:item.cra_obj="{ item }">
          {{ item.cra_obj.first_name }} {{ item.cra_obj.last_name }}
        </template>

        <template v-slot:item.id="{ item }">
          <v-btn
            :title="$t('studies.sites.downloadInfo')" class="px-2" color="blue darken-2" dark small style="min-width: unset"
            @click.prevent="downloadFile($axios, $toast, item.site_instructions_path, 'Instructions.pdf')"
          >
            <v-icon small>event_note</v-icon>
          </v-btn>
          <v-btn
            :title="$t('studies.sites.downloadAgreement')" class="px-2" color="blue darken-2" dark small style="min-width: unset"
            @click.prevent="downloadFile($axios, $toast, item.contract_path, 'PatientForm.pdf')"
          >
            <v-icon small>event_available</v-icon>
          </v-btn>
          <v-btn @click="handleEditSite(item)" class="px-2" color="primary" small style="min-width: unset">
            <v-icon small>edit</v-icon>
          </v-btn>
          <v-btn @click="openDeleteDialog(item)" class="px-2" color="error" small style="min-width: unset">
            <v-icon small>delete</v-icon>
          </v-btn>
        </template>
      </v-data-table>

      <v-dialog max-width="800px" v-model="siteFormDialog">
        <template v-slot:activator="{ on }">
          <v-btn
            @click="clearSite"
            class="mb-2"
            color="primary"
            dark v-on="on"
          >
            {{ $t('studies.sites.newSite') }}
          </v-btn>
        </template>

        <SiteForm :site="editedSite" @saved="handleSiteSaved"/>
      </v-dialog>

      <v-dialog max-width="400px" v-model="deleteSiteDialog">
        <v-card>
          <v-card-title class="headline">
            {{ $t('studies.sites.deleteSite') }} {{ deletedSite ? deletedSite.title : '' }}?
          </v-card-title>
          <v-card-text>{{ $t('studies.sites.reallyDelete') }}</v-card-text>
          <v-card-actions>
            <v-spacer/>
            <v-btn @click="deleteSiteDialog = false" color="gray" text>{{ $t('common.keep') }}</v-btn>
            <v-btn @click="handleDeleteSite" color="red" text>{{ $t('common.delete') }}</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-card-text>
  </v-card>
</template>

<script>
  import { mapActions, mapMutations, mapState } from 'vuex'
  import SiteForm from '~/components/study/sites/SiteForm'
  import downloadFile from '~/helpers/downloadFile'

  export default {
    name: 'SiteList',
    components: { SiteForm },
    computed: {
      ...mapState({
        siteList: state => state.sites.siteList,
      }),
      tableHeaders() {
        return [
          { value: 'title', text: this.$t('common.siteNr') },
          { value: 'cra_obj', text: this.$t('users.cra') },
          { value: 'expected_patients', text: this.$t('site.expectedPatients') },
          { value: 'id', text: '' },
        ]
      }
    },
    data() {
      return {
        deletedSite: null,
        deleteSiteDialog: false,
        editedSite: {},
        selected: [],
        siteFormDialog: false
      }
    },
    methods: {
      ...mapActions({
        deleteSite: 'sites/deleteSite',
        getSiteList: 'sites/getSiteList',
        updateSite: 'sites/updateSite'
      }),
      ...mapMutations({
        clearSite: 'sites/clearSite',
        setSite: 'sites/setSite'
      }),
      downloadFile: downloadFile,
      async handleDeleteSite() {
        try {
          await this.deleteSite(this.deletedSite?.id)
          this.$toast.success(this.$t('common.deletedSuccessfully'))
          this.deleteSiteDialog = false
          this.getSiteList()
        } catch (e) {
          this.$toast.error(e.message)
        }
      },
      handleEditSite(site) {
        this.setSite({ ...site, cra: site.cra_obj.id })
        this.siteFormDialog = true
      },
      handleSiteSaved() {
        this.siteFormDialog = false
        this.getSiteList(this.$route.params.id)
      },
      openDeleteDialog(site) {
        this.deletedSite = site
        this.deleteSiteDialog = true
      }
    },
    mounted() {
      this.getSiteList(this.$route.params.id)
    }
  }
</script>


