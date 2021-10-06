<template>
  <v-card class="mb-4">
    <v-card-title>
      {{ $t('studies.finance.topUpRequests') }}
    </v-card-title>

    <v-card-text>
      <v-data-table
        :footer-props="{
          'items-per-page-options': [10, 20, 50, -1]
        }"
        :headers="tableHeaders"
        :items="topUpList"
        :items-per-page="20"
      >
        <template v-slot:item.created_at="{ item }">
          {{ new Date(item.created_at).toLocaleString() }}
        </template>
        <template v-slot:item.file="{ item }">
          <v-icon color="primary" @click="downloadFile($axios, $toast, item.file, 'TopupRequest.pdf')">
            cloud_download
          </v-icon>
        </template>
      </v-data-table>
    </v-card-text>
  </v-card>
</template>

<script>
  import { mapActions, mapState } from 'vuex'
  import downloadFile from '~/helpers/downloadFile'

  export default {
    name: 'TopUpTable',
    computed: {
      ...mapState({
        topUpList: state => state.topups.topUpList
      }),
      tableHeaders() {
        return [
          { value: 'created_at', text: this.$t('common.date') },
          { value: 'amount', text: this.$t('common.amount') },
          { value: 'file', text: this.$t('common.file') }
        ]
      }
    },
    methods: {
      ...mapActions({
        getTopUpList: 'topups/getTopUpList'
      }),
      downloadFile: downloadFile
    },
    created() {
      this.getTopUpList()
    }
  }
</script>
