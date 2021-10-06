<template>
  <v-row v-if="patient.payment_type === 'POST'">
    <FormInput
      :breakpoints="{ sm: 6, md: 4, lg: 3 }"
      field="name"
      :label="$t('address.name')"
      required
      type="text"
      :value="patient.name"
      @change="updatePatientField($event)"
    />

    <v-col sm="6" md="8" lg="9" class="py-0">
      <vue-google-autocomplete
        classname="google-autocomplete-input"
        :country="['cz', 'sk']"
        id="map"
        :placeholder="$t('address.googleAutocompletePlaceholder')"
        @placechanged="handleAddressSelected"
      />

    </v-col>

<!--    <v-col class="py-0" cols="12" md="6">-->
<!--      <v-autocomplete-->
<!--        :error="!!errorObject['street']"-->
<!--        :error-messages="errorObject['street']"-->
<!--        :items="streetOptions"-->
<!--        :label="$t('address.address')"-->
<!--        :loading="loadingStreet"-->
<!--        :search-input.sync="addressSearch"-->
<!--        @change="handleAddressSelected($event)"-->
<!--        autocomplete="new"-->
<!--        clearable-->
<!--        dense-->
<!--        hide-no-data-->
<!--        outlined-->
<!--        v-model="selectedAddress"-->
<!--      />-->
<!--    </v-col>-->
  </v-row>
</template>

<script>
  import { mapActions, mapMutations, mapState } from 'vuex'
  import VueGoogleAutocomplete from 'vue-google-autocomplete'
  import FormInput from '~/components/partials/FormInput'
  import getStreetNumberFromGoogleResults from '~/helpers/getStreetNumberFromGoogleResults'

  export default {
    name: 'AddressForm',
    components: { FormInput, VueGoogleAutocomplete },
    computed: {
      ...mapState({
        loadingStreet: state => state.address.loadingStreet,
        street: state => state.address.street,
        streetOptions: state => state.address.streetOptions,

        errorObject: state => state.errors.errorObject,
        patient: state => state.patients.patient
      })
    },
    data: () => ({
      addressSearch: '',
      selectedAddress: null
    }),

    methods: {
      ...mapActions({
        getSuggestion: 'address/getSuggestion',
      }),
      ...mapMutations({
        updateAddressField: 'address/updateAddressField',
        updatePatientField: 'patients/updatePatientField'
      }),
      handleAddressSelected(addressResult, placeResult) {
        if (!addressResult) return

        this.updatePatientField({ field: 'street', value: addressResult.route || '' })
        this.updatePatientField({ field: 'street_number', value: getStreetNumberFromGoogleResults(addressResult, placeResult) })
        this.updatePatientField({ field: 'city', value: addressResult.locality || '' })
        this.updatePatientField({ field: 'zip', value: addressResult.postal_code || '' })
      }
    },
    // mounted() {
    //   setTimeout(() => {
    //     var service = new google.maps.places.PlacesService(this.$refs.placesInput)
    //   }, 2000)
    //
    // },
    // head: {
    //   script: [
    //     { hid: 'GM', src: `https://maps.googleapis.com/maps/api/js?key=AIzaSyAxOVlyMJ15IF8uFUUq_zZM6Hn7gvPi5j8&libraries=places` }
    //   ]
    // },
    // watch: {
    //   addressSearch (value) {
    //     if (value)
    //       this.getSuggestion(value)
    //   }
    // },
  }
</script>

<style scoped lang="scss">
  .google-autocomplete-input {
    border: 1px solid #9E9E9E;
    border-radius: 4px;
    font-size: 16px;
    height: 40px;
    padding-left: 8px;
    width: 100%;

    &:focus, &:active {
      border-color: #36A693;
      outline-color: #36A693;
    }
  }
</style>
