<template>
  <div v-if="config">
    <WizardBlock :configPart="config.setup"/>
    <WizardBlock :configPart="config.progress"/>
    <WizardBlock :configPart="config.end"/>
  </div>
<!--  <v-stepper v-model="studyStatus" vertical>-->
<!--&lt;!&ndash;    TODO consider this https://vuetifyjs.com/en/components/expansion-panels/#custom-icon&ndash;&gt;-->

<!--    <v-stepper-step :complete="studyStatus > 1" step="1">-->
<!--      {{ $t('studies.setup.step1') }}-->
<!--    </v-stepper-step>-->
<!--    <v-stepper-content step="1">-->
<!--      {{ $t('studies.setup.step1help') }}-->
<!--      <nuxt-link-->
<!--        :to="localePath(study.id ? {name: 'studies-id-general', params: {id: study.id}} : {name: 'studies-new-general'})"-->
<!--      >-->
<!--        <v-btn color="primary">-->
<!--          {{ $t('studies.menu.general') }}-->
<!--        </v-btn>-->
<!--      </nuxt-link>-->
<!--    </v-stepper-content>-->

<!--    <v-stepper-step :complete="studyStatus > 2" step="2">-->
<!--      {{ $t('studies.setup.step2') }}-->
<!--    </v-stepper-step>-->
<!--    <v-stepper-content step="2">-->
<!--      {{ $t('studies.setup.step2help') }}-->
<!--      <nuxt-link :to="localePath({name: 'studies-id-reims', params: {id: study.id}})">-->
<!--        <v-btn color="primary">-->
<!--          {{ $t('studies.menu.reims') }}-->
<!--        </v-btn>-->
<!--      </nuxt-link>-->
<!--    </v-stepper-content>-->

<!--    <v-stepper-step :complete="studyStatus > 3" step="3">-->
<!--      {{ $t('studies.setup.step3') }}-->
<!--    </v-stepper-step>-->
<!--    <v-stepper-content step="3">-->
<!--      {{ $t('studies.setup.step3help') }}-->
<!--      <nuxt-link :to="localePath({name: 'studies-id-visits', params: {id: study.id}})">-->
<!--        <v-btn color="primary" small>-->
<!--          {{ $t('studies.menu.visits') }}-->
<!--        </v-btn>-->
<!--      </nuxt-link>-->
<!--    </v-stepper-content>-->

<!--    <v-stepper-step :complete="studyStatus > 4" step="4">-->
<!--      {{ $t('studies.setup.step4') }}-->
<!--    </v-stepper-step>-->
<!--    <v-stepper-content step="4">-->
<!--      {{ $t('studies.setup.step4help') }}-->
<!--      <nuxt-link :to="localePath({name: 'studies-id-sites', params: {id: study.id}})">-->
<!--        <v-btn color="primary" small>-->
<!--          {{ $t('studies.menu.sites') }}-->
<!--        </v-btn>-->
<!--      </nuxt-link>-->
<!--    </v-stepper-content>-->

<!--    <v-stepper-step :complete="studyStatus > 5" step="5">-->
<!--      {{ $t('studies.setup.step5') }}-->
<!--    </v-stepper-step>-->
<!--    <v-stepper-content step="5">-->
<!--      {{ $t('studies.setup.step5help') }}-->

<!--      <v-btn color="primary" small>-->
<!--        {{ $t('studies.setup.lock') }}-->
<!--      </v-btn>-->
<!--    </v-stepper-content>-->

<!--    <v-stepper-step :complete="studyStatus > 6" step="6">-->
<!--      {{ $t('studies.setup.step6') }}-->
<!--    </v-stepper-step>-->
<!--    <v-stepper-content step="6">-->
<!--      <v-simple-table class="mb-4" style="table-layout: fixed">-->
<!--        <template v-slot:default>-->
<!--          <tbody>-->
<!--          <tr>-->
<!--            <td>{{ $t('studies.setup.step6minimalTopup') }}</td>-->
<!--            <td>-->
<!--              Selected payment frequency: TODO visits<br>-->
<!--              Expected patients:-->
<!--              Total value of items in first 2 visits: TODO CZK-->
<!--            </td>-->
<!--          </tr>-->
<!--          <tr>-->
<!--            <td>{{ $t('studies.setup.step6furtherTopup') }}</td>-->
<!--            <td>-->
<!--              TODO * TODO * 50 % = TODO CZK-->
<!--              10 % fee = TODO CZK-->
<!--              Total TODO CZK-->
<!--            </td>-->
<!--          </tr>-->
<!--          </tbody>-->
<!--        </template>-->
<!--      </v-simple-table>-->

<!--      <div class="d-flex flex-column align-items-center">-->
<!--        Topup TODO CZK for study activation-->
<!--        <v-btn color="primary" large>-->
<!--          {{ $t('studies.setup.createOrder') }}-->
<!--        </v-btn>-->
<!--        <small>{{ $t('studies.setup.step5willStart') }}</small>-->
<!--      </div>-->
<!--    </v-stepper-content>-->
<!--  </v-stepper>-->
</template>

<script>
  import { mapActions, mapState } from 'vuex'
  import WizardBlock from '~/components/study/setup/WizardBlock'

  export default {
    name: 'SetupWizard',
    components: { WizardBlock },
    methods: {
      ...mapActions({
        getStudyConfig: 'studyconfig/getStudyConfig'
      })
    },
    created() {
      this.getStudyConfig()
    },
    computed: {
      ...mapState({
        config: state => state.studyconfig.config
      })
    }
  }
</script>

<style scoped>

</style>
