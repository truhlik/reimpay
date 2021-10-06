<template>
  <v-card>
    <v-card-title class="mb-4">
      {{ title ? title : $t('studies.patients.addPatient') }}
    </v-card-title>
    <v-card-text>
      <v-row>
        <FormInput
          :breakpoints="{sm: 6, md: 4, lg: 3}"
          field="number"
          :label="$t('common.patientNr')"
          required
          type="text"
          :value="patient.number"
          @change="updatePatientField($event)"
        />

        <FormSelect
          :breakpoints="{sm: 6, md: 4, lg: 3}"
          field="site"
          :items="siteOptionList"
          :label="$t('common.site')"
          :readonly="updateMode"
          :value="patient.site || siteId"
          @change="updatePatientField($event)"
        />

        <FormSelect
          :breakpoints="{sm: 6, md: 4, lg: 3}"
          field="arm"
          :items="armOptionList"
          :label="$t('studies.patients.armMap')"
          :readonly="updateMode"
          :value="patient.arm"
          @change="updatePatientField($event)"
        />

        <FormSelect
          :breakpoints="{sm: 6, md: 4, lg: 3}"
          field="payment_type"
          :items="paymentInfoOptionList"
          :label="$t('studies.patients.paymentForm')"
          :value="patient.payment_type"
          @change="updatePatientField($event)"
        />

        <FormInput
          :breakpoints="{sm: 6, md: 4, lg: 3}"
          :label="$t('studies.patients.bankNr')"
          field="payment_info"
          required
          :rules="[
            value => (value ? /^\d*(-?)\d*\/[0-9]{4}$/.test(value) : true) || $t('common.invalidBankAccount')
          ]"
          type="text"
          :value="patient.payment_info"
          v-if="patient.payment_type === 'BANK'"
          @change="updatePatientField($event)"
        />
      </v-row>

      <AddressForm/>

      <v-row>
        <v-col class="text-center">
          <v-btn @click="handleSavePatient" class="px-10" color="primary" x-large>
            {{ $t('common.save') }}
          </v-btn>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>
  import { mapActions, mapGetters, mapMutations, mapState } from 'vuex'

  import AddressForm from '~/components/study/patients/AddressForm'
  import FormInput from '~/components/partials/FormInput'
  import FormSelect from '~/components/partials/FormSelect'

  export default {
    name: 'PatientForm',
    components: { AddressForm, FormInput, FormSelect },
    props: {
      siteId: {
        type: Number,
        required: false
      },
      title: {
        type: String,
        required: false
      },
      updateMode: {
        type: Boolean,
        default: false
      }
    },
    computed: {
      ...mapGetters({
        armOptionList: 'arms/armOptionList',
        siteOptionList: 'sites/siteOptionList',
        paymentInfoOptionList: 'patients/paymentInfoOptionList',
      }),
      ...mapState({
        patient: state => state.patients.patient
      })
    },
    data: () => ({
      cityOptions: [],
      streetOptions: [],
      zipOptions: [],
    }),
    methods: {
      ...mapActions({
        createPatient: 'patients/createPatient',
        getArmList: 'arms/getArmList',
        getSitePatientList: 'sites/getSitePatientList',
        updatePatient: 'patients/updatePatient'
      }),
      ...mapMutations({
        clearErrorObject: 'errors/clearErrorObject',
        clearPatient: 'patients/clearPatient',
        updatePatientField: 'patients/updatePatientField'
      }),
      async handleSavePatient() {
        try {
          this.patient.id ? await this.updatePatient() : await this.createPatient()
          this.$emit('close')
          this.getSitePatientList()
          this.clearPatient()
          this.clearErrorObject()
          if (this.siteId) this.updatePatientField({field: 'site', value: this.siteId})   // TODO is this needed?
        } catch (e) {
          this.$toast.error(e.message)
        }
      }
    },
    mounted() {
      this.getArmList()
      // sites loaded in patients.vue page

      this.updateMode ? this.updatePatientField({ field: 'number', value: '' }) : this.clearPatient()

      if (this.siteId) this.updatePatientField({ field: 'site', value: this.siteId })
    }
  }
</script>

<style scoped>

</style>
