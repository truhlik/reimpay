<template>
  <transition name="fade" mode="out-in" appear>
    <div>
      <VisitPaginator/>

      <v-row :key="visit.id" v-for="visit of visitList">
        <transition name="fade" mode="out-in" appear>
          <VisitCard :visit="visit"/>
        </transition>
      </v-row>

      <VisitPaginator/>
    </div>
  </transition>
</template>

<script>
  import { mapActions, mapState } from 'vuex'
  import Loader from '~/components/partials/Loader'
  import VisitCard from '~/components/study/visits/VisitCard'
  import VisitPaginator from '~/components/study/visits/VisitPaginator'

  export default {
    name: 'VisitTables',
    components: { Loader, VisitCard, VisitPaginator },
    computed: {
      ...mapState({
        loading: state => state.visits.loading,
        visitList: state => state.visits.visitList
      })
    },
    methods: {
      ...mapActions({
        getStudyItemList: 'studyitems/getStudyItemList'
      })
    },
    created() {
      this.getStudyItemList()
    }
  }
</script>

<style scoped>

</style>
