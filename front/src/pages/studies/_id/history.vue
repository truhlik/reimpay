<template>
  <div>
    <PageTitle :heading=title :icon=icon :subheading=subheading show-study-info/>

    <StudyMenu :isNew="false" :studyId="$route.params.id" active-item="history"/>

    <v-card>
      <v-data-table
        :expanded.sync="expanded"
        :options="{
          itemsPerPage: historyPagination.page_size,
          page: historyPagination.page,
        }"
        :footer-props="{
          'items-per-page-options': [20, 50, 100, 200]
        }"
        :headers="tableHeaders"
        item-key="created_at"
        :items="historyList"
        :server-items-length="historyPagination.count || 0"
        disable-sort
        single-expand
        show-expand
        @update:items-per-page="handlePageSizeChanged"
        @update:page="handlePageChanged"
      >
        <template v-slot:expanded-item="{ headers, item }">
          <td :colspan="headers.length" class="py-3">
            <div :key="`${item.id}-${item.index}`" v-for="updateData in item.update_data">
              <strong>{{ item.action }}</strong>
              <span>
                {{ updateData.field }} {{ $t('common.from') }} {{ updateData.old }} {{ $t('common.to') }} {{ updateData.new }}
              </span>
            </div>
            <div v-if="!item.update_data">{{ $t('common.noExtraData') }}</div>
          </td>
        </template>
        <template v-slot:item.created_at="{ item }">
          {{ new Date(item.created_at).toLocaleString() }}
        </template>
        <template v-slot:item.action="{ item }">
          {{ item.content_type }} {{ item.obj_name }} {{ item.action }}
        </template>
      </v-data-table>
    </v-card>
  </div>
</template>

<script>
  import { mapActions, mapMutations, mapState } from 'vuex'
  import PageTitle from '~/components/partials/PageTitle'
  import StudyMenu from '~/components/study/StudyMenu'

  export default {
    name: 'history',
    components: { PageTitle, StudyMenu },
    async fetch({store, params}) {
      await store.dispatch('studies/getStudy', params.id);
    },
    computed: {
      ...mapState({
        historyList: state => state.history.historyList,
        historyPagination: state => state.history.historyPagination
      }),
      tableHeaders() {
        return [
          { value: 'created_at', text: this.$t('studies.history.date') },
          { value: 'user', text: this.$t('studies.history.user') },
          { value: 'action', text: this.$t('studies.history.action') },
        ]
      }
    },
    data() {
      return {
        title: this.$t('studies.patients.title'),
        subheading: this.$t('studies.patients.subtitle'),
        icon: 'pe-7s-note2 icon-gradient bg-reimpay',
        expanded: [],
      }
    },
    methods: {
      ...mapActions({
        getHistory: 'history/getHistory'
      }),
      ...mapMutations({
        setPaginationPage: 'history/setHistoryPaginationPage',
        setPaginationSize: 'history/setHistoryPaginationSize'
      }),
      handlePageChanged(pageNumber) {
        this.setPaginationPage(pageNumber)
        this.getHistory()
      },
      handlePageSizeChanged(pageSize) {
        this.setPaginationSize(pageSize)
        this.getHistory()
      },
    },
    created() {
      this.getHistory()
    }
  }
</script>

<style scoped>

</style>
