<template>
  <div>
    <PageTitle
      :heading="title"
      :subheading=subheading
      :icon=icon
      :buttonText="isAdmin ? $t('common.newStudy') : null"
      @btnClick="$router.push(localePath({name: 'studies-new-setup'}))"
    />
    <v-card>
      <v-card-text>
        <v-data-table
          :headers="tableHeaders"
          hide-default-footer
          :items="studyList"
        >
          <template v-slot:item.identifier="{ item }">
            <nuxt-link
              :to="localePath({ name: isAdmin ? 'studies-id-setup' : 'studies-id-patients', params: { id: item.id }})"
            >
              {{ item.identifier }}
            </nuxt-link>
          </template>
          <template v-slot:item.id="{ item }">
            <nuxt-link
              :to="localePath({name:'studies-id-setup', params: {id: item.id}})"
            >
              <v-btn class="px-2" color="primary" small style="min-width: unset">
                <v-icon small>edit</v-icon>
              </v-btn>
            </nuxt-link>
            <v-btn @click.stop="openDeleteDialog(item.id)" class="px-2" color="error" small style="min-width: unset">
              <v-icon small>delete</v-icon>
            </v-btn>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>

    <v-dialog
      v-model="deleteDialog"
      max-width="290"
    >
      <v-card>
        <v-card-title class="headline">
          {{ $t('common.deleteConfirmTitle') }}
        </v-card-title>
        <v-card-text>
          {{ $t('common.deleteConfirmText') }}.
        </v-card-text>

        <v-card-actions>
          <v-spacer/>

          <v-btn @click="deleteDialog = false" color="gray" text>
            {{ $t('common.keep') }}
          </v-btn>

          <v-btn @click="deleteStudyFromDialog()" color="red" text>
            {{ $t('common.delete') }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
  import { mapActions, mapGetters, mapState } from 'vuex'
  import PageTitle from '~/components/partials/PageTitle'

  export default {
    name: "index",
    components: { PageTitle },
    computed: {
      ...mapGetters({
        isAdmin: 'account/isAdmin'
      }),
      ...mapState({
        studyList: (state) => state.studies.studyList
      }),
      tableHeaders() {
        let tableColumns = [
          { value: 'status', text: this.$t('study.status') },
          { value: 'number', text: this.$t('study.hash') },
          { value: 'identifier', text: this.$t('study.name') },
          { value: 'active_patients', text: this.$t('study.activePatients') },
          { value: 'credit', text: this.$t('study.credit') },
          { value: 'paid', text: this.$t('study.paid') },
          { value: 'date_launched', text: this.$t('study.dateLaunched') },
          { value: 'date_last_visit', text: this.$t('study.dateLastVisit') }
        ]

        if (this.isAdmin) {
          tableColumns.push({ value: 'id', text: '' })
        }

        return tableColumns
      }
    },
    data() {
      return {
        title: this.$t('studyList.title'),
        subheading: this.$t('studyList.subtitle'),
        icon: 'pe-7s-note2 icon-gradient bg-reimpay',

        deleteDialog: false,
        deletedStudyId: null
      }
    },
    methods: {
      ...mapActions({
        deleteStudy: 'studies/deleteStudy',
        getStudyList: 'studies/getStudyList'
      }),
      async deleteStudyFromDialog() {
        this.deleteDialog = false
        await this.deleteStudy(this.deletedStudyId)
        this.getStudyList()
      },
      openDeleteDialog(itemId) {
        this.deleteDialog = true
        this.deletedStudyId = itemId
      },
    },
    mounted() {
      this.getStudyList()
    }
  }
</script>

<style scoped>

</style>
