<template>
  <v-col :lg="breakpoints.lg" :md="breakpoints.md" :sm="breakpoints.sm" :xl="breakpoints.xl" class="py-0" cols="12">
    <v-autocomplete
      autocomplete="new"
      :chips="multiple"
      :clearable="clearable"
      :deletable-chips="multiple"
      dense
      :disabled="readonly"
      :error="!!errorObject[field]"
      :error-messages="errorObject[field]"
      :hide-details="hideDetails"
      :id="field"
      :items="items"
      :key="value || 'not working workaround'"
      :label="label"
      :multiple="multiple"
      :readonly="readonly"
      :required="required"
      :rules="rules"
      :search-input="value"
      :value="value"
      @change="$emit('change', {field: field, value: $event})"
      @keydown="$emit('input', {field: field, value: $event})"
      color="primary"
      outlined
    />
  </v-col>
</template>

<script>
  import { mapState } from 'vuex'

  export default {
    name: "FormAutocomplete",
    props: {
      breakpoints: {
        type: Object,
        required: false,
        default: () => ({
          sm: 12, md: 6, lg: 6, xl: 6
        })
      },
      clearable: {
        type: Boolean,
        default: false
      },
      dense: {
        type: Boolean,
        default: false
      },
      field: {
        type: String,
        required: false
      },
      hideDetails: {
        type: Boolean,
        default: false,
      },
      items: {
        type: Array,
        required: true
      },
      label: {
        type: String,
        required: false
      },
      multiple: {
        type: Boolean,
        default: false
      },
      required: {
        type: Boolean,
        default: false,
      },
      readonly: {
        type: Boolean,
        default: false,
      },
      value: {
        default: null,
      },
      rules: {
        type: Array,
        required: false
      },
    },
    computed: {
      ...mapState({
        errorObject: state => state.errors.errorObject
      }),
    },
  }
</script>
