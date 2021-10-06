<template>
  <div>
    <PageTitle
      :heading="company.name || title"
      :subheading=subheading
      :icon=icon
    />
    <v-card :title="title" class="main-card mb-4">
      <v-card-text>
        <CompanySummary/>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
  import { mapState } from 'vuex'
  import CompanySummary from '~/components/admin/company/CompanySummary'
  import PageTitle from '~/components/partials/PageTitle'

  export default {
    name: 'user',
    components: { CompanySummary, PageTitle },
    async fetch({store}) {
      await store.dispatch('company/getCompanyForUser')
    },
    computed: {
      ...mapState({
        company: state => state.company.company,
      })
    },
    data() {
      return {
        title: this.$t('company.title'),
        subheading: this.$t('company.subtitle'),
        icon: 'pe-7s-home icon-gradient bg-reimpay',

        formValid: null,
      }
    },
  }
</script>

