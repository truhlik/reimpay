<template>
  <v-col class="mb-4">
    <v-card class="visit-card">
      <span class="visit-order">
        <span v-if="visit.visit_type === 'REGULAR'">{{ visit.order }}</span>
        <span v-if="visit.visit_type === 'UNSCHEDULED'">UV</span>
        <small v-if="visit.visit_type === 'DISCONTINUAL'">DISC</small>
      </span>
      <v-card-title>
        <span>
          <span v-if="!renamingVisit">
            {{ visit.title }}

            <v-btn @click="enableRenameInput" color="primary" small text>
              {{ visit.title ? $t('common.rename') : $t('common.addName') }}
            </v-btn>
          </span>
          <span class="d-inline-flex align-items-center" v-else>
            <v-text-field
              dense
              :hide-details="true"
              ref="renameInput"
              v-model="visitTitle"
              @blur="renamingVisit = false"
              @change="handlePatchVisit({ field: 'title', value: visitTitle })"
            />
          </span>
        </span>
        <v-spacer/>
        <v-btn class="delete-button" color="red" dark small v-if="visit.visit_type === 'REGULAR'" @click="handleDeleteVisit">
          {{ $t('common.delete') }}
        </v-btn>
      </v-card-title>

      <v-card-text>
        <v-row>
          <v-col cols="12" sm="8">
            <v-row :key="`${visit.id}-${visitItem.id}`" class="align-items-top mb-2" v-for="visitItem of visit.visit_items">
              <FormSelect
                :breakpoints="{lg: 5}"
                dense
                hideDetails
                :items="studyItemOptionList"
                :placeholder="`${$t('studies.visits.selectReim')}...`"
                :value="visitItem.study_item"
                @change="handleUpdateVisitItem(visitItem, $event.value)"
              />
              <v-col class="d-flex align-items-top p-2" lg="3">
                {{ visitItem.study_item_obj.price }} {{ $t('currencies.czk') }}
                <v-spacer/>
                <v-icon @click="handleDeleteVisitItem(visitItem.id)" class="cursor-pointer" style="height: 20px">
                  delete
                </v-icon>
              </v-col>
            </v-row>
            <v-row class="align-items-center">
              <FormSelect
                :breakpoints="{lg: 5}"
                dense
                :items="studyItemOptionList"
                :placeholder="`${$t('studies.visits.selectReim')}...`"
                v-if="addingNewItem"
                @change="handleCreateVisitItem($event.value)"
              />
              <v-col class="p-0" v-else>
                <v-btn @click="addingNewItem = true" color="primary" small text>
                  +{{ $t('studies.visits.addReim') }}
                </v-btn>
              </v-col>
            </v-row>
          </v-col>
          <v-col cols="12" sm="4" v-if="visit.visit_type === 'UNSCHEDULED'">
            <v-row>
              <FormInput
                :breakpoints="{sm: 12, md: 12, lg: 12, xl: 12}"
                :label="$t('studies.visits.maxUnscheduled')"
                :value="visit.number"
                @change="handlePatchVisit($event)"
                field="number"
                :rules="[
                  value => !isNaN(value) && value >= 0 || $t('errors.positiveNumber')
                ]"
                type="number"
              />
            </v-row>
          </v-col>
        </v-row>
      </v-card-text>
      <span class="move-button-container d-flex flex-column" v-if="visit.visit_type === 'REGULAR'">
        <v-btn
          :disabled="changingOrder || visit.order < 2"
          color="primary"
          class="mb-2"
          small
          @click="handlePatchVisit({field: 'order', value: visit.order - 1})"
        >
          <v-icon>keyboard_arrow_up</v-icon>
        </v-btn>
        <v-btn
          :disabled="changingOrder || visit.id === lastRegularVisitId"
          color="primary"
          small
          @click="handlePatchVisit({field: 'order', value: visit.order + 1})"
        >
          <v-icon>keyboard_arrow_down</v-icon>
        </v-btn>
      </span>
    </v-card>

    <VisitCardBottomActions :visit="visit" v-if="visit.visit_type === 'REGULAR'"/>
  </v-col>
</template>

<script>
  import { mapActions, mapGetters, mapMutations } from 'vuex'
  import FormInput from '~/components/partials/FormInput'
  import FormSelect from '~/components/partials/FormSelect'
  import VisitCardBottomActions from '~/components/study/visits/VisitCardBottomActions'

  export default {
    name: 'VisitTables',
    components: { FormInput, FormSelect, VisitCardBottomActions },
    props: {
      visit: {
        type: Object,
        required: true
      }
    },
    computed: {
      ...mapGetters({
        lastRegularVisitId: 'visits/lastRegularVisitId',
        studyItemOptionList: 'studyitems/studyItemOptionList'
      })
    },
    data: () => ({
      addingNewItem: false,
      changingOrder: false,
      renamingVisit: false,
      visitTitle: ''
    }),
    methods: {
      ...mapActions({
        createVisitItem: 'visits/createVisitItem',
        deleteVisit: 'visits/deleteVisit',
        deleteVisitItem: 'visits/deleteVisitItem',
        getVisitList: 'visits/getVisitList',
        partialUpdateVisit: 'visits/partialUpdateVisit',
        updateVisitItem: 'visits/updateVisitItem'
      }),
      ...mapMutations({
        updateVisitField: 'visits/updateVisitField'
      }),
      enableRenameInput() {
        this.renamingVisit = true
        this.$nextTick(            // nextTict potřebujeme kvůli tomu, že je tam v-if a musíme nejdřív rerenderovat
          () => this.$refs.renameInput.focus()
        )
      },
      async handleCreateVisitItem(reimId) {
        if (!reimId) return

        await this.createVisitItem({visit: this.visit.id, study_item: reimId})
        this.addingNewItem = false

        this.getVisitList()
      },
      async handleDeleteVisit() {
        await this.deleteVisit(this.visit.id)
        this.getVisitList()
      },
      async handleDeleteVisitItem(visitItemId) {
        await this.deleteVisitItem(visitItemId)
        this.getVisitList()
      },
      async handlePatchVisit({field, value}) {
        if (value === null || value === undefined) return

        if (field === 'order')
          this.changingOrder = true

        if (field === 'title')
          this.renamingVisit = false

        let patchData = {id: this.visit.id};
        patchData[field] = value

        await this.partialUpdateVisit(patchData)
        await this.getVisitList()

        this.changingOrder = false
      },
      async handleUpdateVisitItem(visitItem, reimId) {
        const newVisitItem = {...visitItem, study_item: reimId};
        await this.updateVisitItem(newVisitItem)
        this.getVisitList();
      },
    },
    mounted() {
      this.visitTitle = this.visit.title

      if (!this.visit.visit_items.length)
        this.addingNewItem = true
    }
  }
</script>

<style scoped lang="scss">
  .visit-card {
    padding: 0 60px;

    @media (max-width: 576px) {
      padding: 0 20px;
    }
  }
  .visit-order {
    color: lightgray;
    display: inline-block;
    font-size: 50px;
    left: 0;
    position: absolute;
    text-align: center;
    width: 74px;

    small {
      font-size: 60%;
    }

    @media (max-width: 576px) {
      font-size: 25px;
      width: 32px;
    }
  }
  .delete-button {
    position: absolute;
    right: 10px;
    top: 20px;

    @media (max-width: 576px) {
      position: static
    }
  }
  .move-button-container {
    position: absolute;
    right: 30px;
    transform: translateY(-50%);
    top: 50%;

    @media (max-width: 576px) {
      position: static;
      margin-top: 2rem;
    }
  }
</style>
