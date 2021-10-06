<template>
  <v-card class="mb-4">
    <v-card-title>
      {{ $t('common.basicInfo') }}
    </v-card-title>
    <v-card-text>
      <v-row>
        <FormInput
          :label="$t('study.hash')" :value="study.number" field="number" type="text"
          @change="updateStudyField($event)"
        />
        <FormInput
          :label="$t('study.name')" :value="study.identifier" field="identifier" type="text"
          @change="updateStudyField($event)"
        />
        <FormSelect
          :items="operatorOptions"
          :label="$t('study.operator')"
          :value="study.operator"
          @change="handleUpdateOperator($event)"
          field="operator"
        />
        <FormInput
          :label="$t('study.sponsorName')"
          :readonly="study.operator !== 'CRO'"
          :value="study.sponsor_name"
          @change="updateStudyField($event)"
          field="sponsor_name"
        />
        <FormInput
          field="bank_account"
          :label="$t('study.bankAccount')"
          :rules="[
            value => (value ? /^\d*(-?)\d*\/[0-9]{4}$/.test(value) : true) || $t('common.invalidBankAccount')
          ]"
          type="text"
          :value="study.bank_account"
          @change="updateStudyField($event)"
        />
        <v-col class="py-0" lg="6">
          <v-textarea
            :counter="1000"
            :label="$t('study.notes')"
            outlined
            :rules="[v => !v || v.length < 1001 || $t('errors.max1000chars') ]"
            :value="study.notes"
            @change="updateStudyField({field: 'notes', value: $event})"
          />
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>
  import { mapMutations, mapState } from 'vuex';
  import FormInput from '~/components/partials/FormInput'
  import FormSelect from '~/components/partials/FormSelect'

  export default {
    name: 'SetupInfo',
    components: { FormInput, FormSelect },
    computed: {
      ...mapState({
        study: state => state.studies.study,
      }),
      operatorOptions() {
        return [
          { value: 'CRO', text: 'CRO' },
          { value: 'SPONSOR', text: 'SPONSOR' },
        ]
      }
    },
    methods: {
      ...mapMutations({
        updateStudyField: 'studies/updateStudyField'
      }),
      handleUpdateOperator(updateObj) {
        this.updateStudyField(updateObj)

        if (updateObj.value !== 'CRO')
          this.updateStudyField({ field: 'sponsor_name', value: '' })
      }
    }
  }
</script>


