<template>
  <v-row class="mb-4">
    <v-col cols="12">
      <h5>{{ $t('common.location') }}</h5>
    </v-col>

    <FormInput
      type="text" :label="$t('location.street')" field="street" :value="editedObject.street"
      @change="$emit('addressChange',$event)"
    />
    <FormInput
      type="text" :label="$t('location.city')" field="city" :value="editedObject.city"
      @change="$emit('addressChange',$event)"
    />
    <FormInput
      type="text" :label="$t('location.postalCode')" field="zip" :value="editedObject.zip"
      @change="$emit('addressChange',$event)"
    />
  </v-row>
</template>

<script>
  import FormInput from "~/components/partials/FormInput"

  export default {
    name: "LocationForm",
    components: {
      FormInput
    },
    props: {
      editedObject: {
        type: Object,
        required: true
      }
    }
  }
</script>

<style scoped>

</style>
