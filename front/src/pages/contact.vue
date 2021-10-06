<template>
  <div>
    <PageTitle
      :heading="$t('contact.form')"
      :subheading="$t('contact.subtitle')"
      icon="pe-7s-info icon-gradient bg-reimpay"
    />
    <ContactForm/>
  </div>
</template>

<script>
  import ContactForm from '~/components/ContactForm'
  import PageTitle from '~/components/partials/PageTitle'

  export default {
    name: 'contact',
    components: { ContactForm, PageTitle }
  }
</script>

<style scoped>

</style>
