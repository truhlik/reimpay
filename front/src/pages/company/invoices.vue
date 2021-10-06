<template>
  <div>
    <PageTitle :heading="title" :icon=icon :subheading=subheading />

    <InvoiceTable/>
  </div>
</template>

<script>
  import PageTitle from '~/components/partials/PageTitle'
  import InvoiceTable from '~/components/admin/invoices/InvoiceTable'

  export default {
    name: 'invoices',
    components: { PageTitle, InvoiceTable },
    data() {
      return {
        title: this.$t('invoices.title'),
        subheading: this.$t('invoices.subtitle'),
        icon: 'pe-7s-news-paper icon-gradient bg-reimpay',
      }
    }
  }
</script>
