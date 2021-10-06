<template>
  <v-col :lg="breakpoints.lg" :md="breakpoints.md" :sm="breakpoints.sm" :xl="breakpoints.xl" class="py-0" cols="12">
    <v-text-field
      autocomplete="new"
      color="primary"
      dense
      :disabled="readonly"
      :id="field"
      :error="!!errorObject[field]"
      :error-messages="errorObject[field]"
      :hint="hint"
      :label="label"
      :min="min"
      outlined
      :persistent-hint="!!hint"
      :readonly="readonly"
      :required="required"
      :rules="rules"
      :type="type"
      :value="value"
      @change="$emit('change', {field: field, value: $event})"
      @input="$emit('input', {field: field, value: $event})"
    />
  </v-col>
</template>

<script>
  import { mapState } from 'vuex'

  export default {
    name: "FormInput",
    props: {
      breakpoints: {
        type: Object,
        required: false,
        default: () => ({
          sm: 12, md: 6, lg: 6, xl: 6
        })
      },
      field: {
        type: String,
        required: false
      },
      hint: {
        type: String,
        required: false
      },
      label: {
        type: String,
        required: false
      },
      min: {
        type: Number,
        required: false
      },
      type: {
        type: String,
        default: 'text'
      },
      readonly: {
        type: Boolean,
        default: false,
      },
      required: {
        type: Boolean,
        default: false,
      },
      rules: {
        type: Array,
        required: false
      },
      value: {
        default: null,
      },
    },
    computed: {
      ...mapState({
        errorObject: state => state.errors.errorObject
      }),
    },
  }
</script>
