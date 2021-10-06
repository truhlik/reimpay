<template>
  <div>
    <PageTitle :heading=title :subheading=subheading :icon=icon />
    <v-card :title="title" class="main-card mb-4">
      <v-row class="mb-4" v-if="company.members.length">
        <v-col cols="12">
          <h5>{{ $t('common.basicInfo') }}</h5>
        </v-col>
        <FormInput
          type="text" :label="$t('auth.firstName')" :value="company.members[0].first_name" required
        />
        <FormInput
          type="text" :label="$t('auth.lastName')" :value="company.members[0].last_name" required
        />
      </v-row>
    </v-card>
  </div>
</template>

<script>
  import FormInput from '~/components/partials/FormInput'
  import PageTitle from '~/components/partials/PageTitle'

  export default {
    name: 'user',
    components: { FormInput, PageTitle },
    data() {
      return {
        title: this.$t('account.title'),
        subheading: this.$t('account.subtitle'),
        icon: 'pe-7s-id icon-gradient bg-reimpay',

        formValid: null,
      }
    }
  }
</script>

<style scoped>
  :disabled {
    cursor: not-allowed;
  }
</style>

