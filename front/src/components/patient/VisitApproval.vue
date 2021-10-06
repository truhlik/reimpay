<template>
  <div class="mb-5">
    <h3>{{ selectedVisit ? selectedVisit.title : $t('patientDetail.selectVisit') }}</h3>
    <v-card>
      <v-card-text>
        <v-row>
          <v-col cols="12" sm="6" class="d-flex flex-column justify-content-between">
            <div>
              <h4>{{ $t('patientDetail.selectVisitType') }}</h4>
              <v-radio-group v-model="selectedVisit">
                <div v-for="visit in patientDetail.next_visits" class="w-75">
                  <v-radio
                    color="primary"
                    :key="visit.id"
                    :label="`${visit.visit_type} ${visit.visit_type === 'REGULAR' ? `- ${visit.title}` : $t('common.visit')}`"
                    :value="visit"
                  />
                  <small
                    class="d-block mb-1 text-danger"
                    style="margin-top: -10px"
                    v-if="visit.visit_type === 'UNSCHEDULED' && patientDetail.unscheduled_left === 0"
                  >
                    {{ $t('patientDetail.noUnscheduledLeft') }}
                  </small>
                  <hr v-if="visit.visit_type === 'REGULAR' && patientDetail.next_visits.length > 1">
                </div>
              </v-radio-group>
            </div>

            <div v-if="selectedVisit">
              <h4>{{ $t('patientDetail.selectReims') }}</h4>
              <v-checkbox
                hide-details
                :key="`${selectedVisit.id}-${visitItem.id}`"
                :label="visitItem.study_item_obj.title"
                :value="visitItem.id"
                v-for="visitItem of selectedVisit.visit_items"
                v-model="selectedVisitItems"
              />
            </div>

            <div>
              <v-btn
                :disabled="!valid"
                @click="handleApprove"
                class="mt-3"
                color="primary"
                x-large
              >
                {{ $t('patientDetail.approve') }} {{ total }} {{ $t('currencies.czk') }}
              </v-btn>
            </div>
          </v-col>
          <v-col cols="12" sm="6">
            <v-row>
              <v-col cols="12">
                <v-date-picker
                  event-color="primary"
                  no-title
                  :value="dateFromWidget"
                  @change="handleDateWidgetChange"
                />
              </v-col>
              <v-col cols="12" class="d-flex">
                <v-text-field
                  class="mr-2"
                  dense
                  :label="$t('patientDetail.visitDate')"
                  outlined
                  :rules="[
                    value => /^\d{4}-([0]\d|1[0-2])-([0-2]\d|3[01])$/.test(value) || $t('errors.dateFormat'),
                    value => !!value || $t('errors.required')
                  ]"
                  style="max-width: 200px"
                  :value="date"
                  @input="handleDateChange($event)"
                />
                <v-btn
                  class="mt-1"
                  color="primary"
                  text
                  @click="date = new Date().toISOString().substr(0, 10)"
                >
                  {{ $t('common.today') }}
                </v-btn>
              </v-col>
              <v-col class="py-0" cols="12">
                <v-btn
                  color="blue darken-2"
                  dark
                  x-large
                  @click="requestChangeDialog = true"
                >
                  {{ $t('patientDetail.requestChange1') }}<br>
                  {{ $t('patientDetail.requestChange2') }}
                </v-btn>
              </v-col>
            </v-row>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
    <v-dialog v-model="requestChangeDialog" max-width="500px">
      <v-card>
        <v-card-title>
         Požadavek na změnu platebních údajů pacienta
        </v-card-title>
        <v-card-text>
          <p>
            V případě, žádosti o změnu platebních údajů musí pacient znovu vyplnit Souhlas pacienta dle instrukcí
            ReimPay. Informujte pacienta, že všechny zatím nevyplacené náhrady mu budou zaslány až po aktualizaci dle
            nových údajů.
          </p>
          <p>
            Potvrzujete, že pacient poskytl nové platební údaje na příslušném formuláři?
          </p>
        </v-card-text>
        <hr>
        <v-card-title>
          {{ $t('patientDetail.requestChange') }}
        </v-card-title>
        <v-card-text>
          <p>
            {{ $t('patientDetail.confirmRequestChange1') }}
          </p>
          <p>
            {{ $t('patientDetail.confirmRequestChange2') }}
          </p>
        </v-card-text>
        <v-card-actions class="justify-content-end">
          <v-btn text @click="requestChangeDialog = false">{{ $t('common.no') }}</v-btn>
          <v-btn color="primary" @click="handleChangeRequest">{{ $t('common.yes') }}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
  import { mapActions, mapState } from 'vuex'

  export default {
    name: 'VisitApproval',
    computed: {
      ...mapState({
        errorObject: state => state.errors.errorObject,
        patientDetail: state => state.patients.patientDetail
      }),
      total() {
        if (!this.selectedVisitItems.length) return 0

        const visitItemList = this.selectedVisit.visit_items.filter(vi => this.selectedVisitItems.includes(vi.id))

        if (!visitItemList.length) return 0
        if (visitItemList.length === 1) return visitItemList[0].study_item_obj.price

        return visitItemList.filter(vi => this.selectedVisitItems.includes(vi.id))
                            .reduce((accumulator, item) => (accumulator + item.study_item_obj.price), 0)
      },
      valid() {
        return /^\d{4}-([0]\d|1[0-2])-([0-2]\d|3[01])$/.test(this.date)
      }
    },
    data: () => ({
      date: new Date().toISOString().substr(0, 10),
      dateFromWidget: new Date().toISOString().substr(0, 10),
      requestChangeDialog: false,
      selectedVisit: null,
      selectedVisitItems: []
    }),
    methods: {
      ...mapActions({
        createPatientVisit: 'patientvisits/createPatientVisit',
        getPatient: 'patients/getPatient',
        partialUpdatePatient: 'patients/partialUpdatePatient',
      }),
      handleApprove() {
        this.createPatientVisit({
          patient: this.patientDetail.id,
          visit_date: this.date,
          visit_items: this.selectedVisitItems,
          visit_type: this.selectedVisit.visit_type,

        })
          .then(() => {
            this.$toast.success(this.$t('common.savedSuccessfully'))
            this.getPatient(this.patientDetail.id)
          })
          .catch((e) => this.$toast.error(this.errorObject.visit_date || e.message))
      },
      async handleChangeRequest() {
        await this.partialUpdatePatient({id: this.patientDetail.id, change_payment_request: true})
        this.$toast.success(this.$t('common.sentSuccessfully'))
        this.requestChangeDialog = false
      },
      handleDateChange(value) {
        this.date = value
        if (/^\d{4}-([0]\d|1[0-2])-([0-2]\d|3[01])$/.test(value))
          this.dateFromWidget = value     // invalid date would cause app to crash
      },
      handleDateWidgetChange(value) {
        this.date = value
        this.dateFromWidget = value
      }
    },
    created() {
      this.selectedVisit = this.patientDetail.next_visits[0]
    },
    watch: {
      selectedVisit() {
        this.selectedVisitItems = []
      }
    }
  }
</script>
