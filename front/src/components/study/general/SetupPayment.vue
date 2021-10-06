<template>
  <v-card class="mb-4">
    <v-card-title>
      {{ $t('studies.general.payments') }}
    </v-card-title>
    <v-card-text>
      <v-row>
        <v-col class="py-0" cols="6">
          <v-switch
            class="m-0"
            color="primary"
            :label="`${$t('study.bankTransfer')}`"
            :input-value="study.bank_transfer"
            @change="updateStudyField({field: 'bank_transfer', value: $event})"
          />
        </v-col>
        <v-col class="py-0" cols="6">
          <v-switch
            class="m-0"
            color="primary"
            :label="`${$t('study.postOfficeCash')}`"
            :input-value="study.post_office_cash"
            @change="updateStudyField({field: 'post_office_cash', value: $event})"
          />
        </v-col>
        <v-col class="py-0" cols="12">
          <v-row class="align-items-center">
<!--            <v-col sm="6" lg="3" class="py-0">-->
<!--              {{ $t('studies.general.payFrequencyInfo') }}-->
<!--            </v-col>-->
            <v-col sm="3" md="1" class="py-0">
              {{ $t('common.every') }}
            </v-col>
            <FormInput
              :breakpoints="{ sm: 6, md: 3 }"
              :label="$t('study.payFrequency')"
              :min="1"
              :value="study.pay_frequency"
              class="py-0"
              field="pay_frequency"
              :rules="[
                value => !isNaN(value) && value > 0 || $t('errors.positiveNumber')
              ]"
              type="number"
              @change="updateStudyField($event)"
            />
            <v-col sm="3" md="1" class="py-0">
              {{ $t('common.month') }}
            </v-col>
          </v-row>

          <span>{{ $t('studies.general.invoiceInfo') }}</span>.
          <span>{{ $t('common.pleaseSee') }}</span>
          <a href="/app/docs/pricing2020.pdf" target="_blank" download>
            {{ $t('common.pricing') }}.
          </a>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>
  import { mapMutations, mapState } from 'vuex'
  import FormInput from '~/components/partials/FormInput'
  import { positiveNumbers } from '~/helpers/rules'

  export default {
    name: 'SetupPayment',
    components: { FormInput },
    computed: {
      ...mapState({
        study: state => state.studies.study,
      }),
      data: () => ({
        positiveNumbers: positiveNumbers
      })
    },
    methods: {
      ...mapMutations({
        updateStudyField: 'studies/updateStudyField'
      })
    }
  }
</script>


