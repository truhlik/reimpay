<template>
  <v-card>
    <v-card-title>
      <span class="headline">{{ $t('studies.sites.addNewSite') }}</span>
    </v-card-title>

    <v-card-text>
      <v-row>
        <FormInput
          :breakpoints="{sm: 6, md: 4}"
          field="title"
          :label="$t('common.siteNr')"
          required
          type="text"
          :value="site.title"
          @change="updateField($event)"
        />
        <FormAutocomplete
          :breakpoints="{sm: 6, md: 4}"
          field="cra"
          :items="userCraIdOptions"
          :label="$t('users.cra')"
          :value="site.cra"
          @change="updateField($event)"
        />
        <FormInput
          :breakpoints="{sm: 6, md: 4}" :label="$t('site.expectedPatients')" :value="site.expected_patients" @change="updateField($event)"
          field="expected_patients" required
          type="number"
          :rules="[
            value => !isNaN(value) && value > 0 || $t('errors.positiveNumber')
          ]"
        />
      </v-row>
    </v-card-text>

    <v-card-actions class="d-flex justify-content-center pb-5">
      <v-btn @click="handleSaveSite" color="primary" large>
        {{ $t('common.save') }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
  import {mapActions, mapGetters, mapMutations, mapState} from 'vuex'
  import FormAutocomplete from '~/components/partials/FormAutocomplete'
  import FormInput from '~/components/partials/FormInput'

  export default {
    name: 'SiteForm',
    components: { FormAutocomplete, FormInput },
    computed: {
      ...mapGetters({
        // studyCraOptions: 'company/studyCraOptions'
        userCraIdOptions: 'company/userCraIdOptions'
      }),
      ...mapState({
        site: state => state.sites.site
      })
    },
    methods: {
      ...mapActions({
        createSite: 'sites/createSite',
        // getStudyCraList: 'company/getStudyCraList',
        getUserList: 'company/getUserList',
        updateSite: 'sites/updateSite',
      }),
      ...mapMutations({
        clearErrorObject: 'errors/clearErrorObject',
        clearSite: 'sites/clearSite',
        updateField: 'sites/updateSiteField'
      }),
      async handleSaveSite() {
        try {
          this.site.id ? await this.updateSite() : await this.createSite()
          this.$toast.success(this.$t('common.savedSuccessfully'))
          this.$emit('saved')
          this.clearSite()
          this.clearErrorObject()
        } catch (err) {
          this.$toast.error(this.$t('common.savedNot'))
        }
      },
    },
    created() {
      // this.getStudyCraList()
      this.getUserList()
    }
  }
</script>

<style scoped>

</style>
