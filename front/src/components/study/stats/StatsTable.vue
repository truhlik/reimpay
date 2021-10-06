<template>
  <v-card>
    <v-card-text v-if="stats.stats">
      <div v-if="!Object.keys(stats.stats).length">
        <h5>{{ $t('common.noStatsAvailable') }}</h5>
      </div>
      <div class="mb-10" v-else v-for="siteKey of Object.keys(stats.stats)">
        <h4>{{ $t('common.site') }}: {{ siteKey }}</h4>
        <div class="mb-5 overflow-auto" v-for="armKey of Object.keys(stats.stats[siteKey])">
          <h5>{{ armKey }}</h5>
          <table>
            <tr v-for="(patientData, index) of stats.stats[siteKey][armKey]">
              <th class="bg-primary">{{ Object.keys(patientData)[0] }}</th>
              <td :class="!index ? 'bg-primary' : ''" v-for="columnData of patientData[Object.keys(patientData)[0]]">
                <span class="d-inline-block ml-2" v-if="columnData && columnData.toString().startsWith('http')">
                  <a :href="columnData" target="_blank">
                    <v-btn color="primary" small>
                      <v-icon>add</v-icon>
                    </v-btn>
                  </a>
                </span>
                <span v-else>{{ columnData }}</span>
              </td>
            </tr>
          </table>
        </div>
      </div>
    </v-card-text>
  </v-card>
</template>

<script>
import { mapActions, mapState } from 'vuex'

export default {
  name: 'StatsTable',
  computed: {
    ...mapState({
      stats: state => state.finance.stats
    })
  },
  methods: {
    ...mapActions({
      getStudyStats: 'finance/getStats'
    })
  },
  created() {
    this.getStudyStats()
  }
}
</script>

<style scoped>
  table {
    min-width: 100%;
    table-layout: fixed;
  }

  th, td {
    max-width: 125px;
    min-width: 75px;
    padding: 0.25rem 0.5rem;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .bg-primary {
    color: white
  }
</style>
