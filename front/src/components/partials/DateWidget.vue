<template>
  <v-menu
    :close-on-content-click="false"
    :ref="reference"
    :return-value="value"
    min-width="290px"
    offset-y
    transition="scale-transition"
    v-model="dateWidgetShown"
  >
    <template v-slot:activator="{ on }">
      <v-text-field
        :label="label"
        :value="value"
        @change="$emit('change', $event)"
        autocomplete="new"
        v-on="on"
      />
    </template>
    <v-date-picker
      :value="value"
      @change="$emit('change', $event)"
      @input="dateWidgetShown = false" no-title scrollable
    />
  </v-menu>
</template>

<script>
  export default {
    name: "DateWidget",
    props: {
      value: {
        type: String,
        required: true
      },
      label: {
        type: String,
        required: true
      },
      reference: {
        type: String,
        required: true
      }
    },
    data() {
      return {
        dateWidgetShown: false
      }
    }
  }
</script>

<style scoped>

</style>
