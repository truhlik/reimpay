<template>
  <v-card>
    <v-card-title class="pb-2">
      <small>{{ $t('studies.visits.regularCosts') }}</small>
    </v-card-title>
    <v-card-text class="pb-4">
      <strong style="font-size: 26px">{{ totalCost }}&nbsp;{{ $t('currencies.czk') }}</strong>
    </v-card-text>
  </v-card>
</template>

<script>
  import { mapState } from 'vuex'

  export default {
    name: 'RegularVisitCosts',
    computed: {
      ...mapState({
        arm: state => state.arms.arm,
        visitList: state => state.visits.visitList
      }),
      totalCost() {
        return this.visitList[0]?.visit_items_cost || 0
      }
    },
  }
</script>
