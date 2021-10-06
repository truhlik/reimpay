<template>
  <div>
    <v-btn @click="handleCreateVisit" color="primary" text>
      +{{ $t('studies.visits.addVisit') }}
    </v-btn>
    <v-btn color="primary" :disabled="isCopying" :loading="isCopying" text @click="handleCopyVisit">
      +{{ $t('studies.visits.copyVisit') }}
    </v-btn>
  </div>
</template>

<script>
  import { mapActions } from 'vuex'

  export default {
    name: 'NewVisitDialog',
    props: {
      visit: {
        type: Object,
        required: true
      }
    },
    data: () => ({
      isCopying: false,
    }),
    methods: {
      ...mapActions({
        createVisit: 'visits/createVisit',
        getVisitList: 'visits/getVisitList'
      }),
      async handleCopyVisit() {
        this.isCopying = true
        try {
          await this.createVisit({
            ...this.visit,
            title: `${this.visit.title} (copy)`,
            order: this.visit.order + 1,
            visit_items: this.visit.visit_items.map(vi => ({study_item: vi.study_item})),
            id: undefined
          })
          this.getVisitList()
          this.$toast.success(this.$t('common.savedSuccessfully'))
        } catch (e) {
          this.$toast.error(e)
        }
        this.isCopying = false
      },
      async handleCreateVisit() {
        try {
          await this.createVisit({order: this.visit.order + 1})
          // this.newVisitDialog = false
          this.getVisitList()
          this.$toast.success(this.$t('common.savedSuccessfully'))
        } catch (e) {
          this.$toast.error(e.message)
        }
      },
    }
  }
</script>
