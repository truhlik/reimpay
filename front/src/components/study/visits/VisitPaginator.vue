<template>
  <v-card v-if="visitPagination.num_pages">
    <v-card-text class="font-size-lg">
      <div class="d-flex justify-content-between">
        <strong>
          <span class="color-brand">Total visits:</span> {{ visitPagination.count }}
        </strong>

        <strong>
          <span class="color-brand">Page: </span>
          <span
            :class="pageNum === visitPagination.page ? '' : 'color-brand cursor-pointer'"
            v-for="pageNum in visitPagination.num_pages"
            @click="handleChangePaginationPage(pageNum)"
          >
            {{ pageNum }}
          </span>
        </strong>
      </div>
    </v-card-text>
  </v-card>
</template>

<script>
  import { mapActions, mapMutations, mapState } from 'vuex'
  import Loader from '~/components/partials/Loader'
  import VisitCard from '~/components/study/visits/VisitCard'

  export default {
    name: 'VisitTables',
    components: { Loader, VisitCard },
    computed: {
      ...mapState({
        visitPagination: state => state.visits.visitPagination
      })
    },
    methods: {
      ...mapActions({
        getVisitList: 'visits/getVisitList'
      }),
      ...mapMutations({
        setPaginationPage: 'visits/setPaginationPage'
      }),
      handleChangePaginationPage(pageNum) {
        this.setPaginationPage(pageNum)
        this.getVisitList()
      }
    }
  }
</script>

<style scoped>

</style>
