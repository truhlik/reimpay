<template>
  <v-card>
    <v-card-text>
      <v-row>
        <FormSelect
          :breakpoints="{sm: 6, md: 4}"
          :items="armOptionList"
          :value="arm.id"
          @change="handleChangeArm($event.value)"
        />
        <v-col>
          <v-btn @click="armDialog = true" color="primary" small>
            {{ $t('common.rename') }}
          </v-btn>
          <v-btn @click="deleteArmDialog = true" color="red" dark small>
            {{ $t('common.delete') }}
          </v-btn>
          <v-btn @click="handleAddArm" color="green" dark small>
            {{ $t('studies.visits.addArm') }}
          </v-btn>
        </v-col>
      </v-row>
    </v-card-text>

    <v-dialog max-width="600px" v-model="armDialog">
      <v-card>
        <v-card-title>
          {{ arm.id ? $t('common.rename') : $t('studies.visits.addArm') }}
        </v-card-title>
        <v-card-text>
          <v-row class="pt-4">
            <FormInput
              :breakpoints="{md: 6}" :label="$t('common.title')" :value="arm.title" @input="updateArmField($event)"
              field="title" required
            />
            <v-col class="py-0">
              <v-btn @click="handleSaveArm" color="primary" large>
                {{ $t('common.save') }}
              </v-btn>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
    </v-dialog>

    <v-dialog max-width="290" v-model="deleteArmDialog">
      <v-card>
        <v-card-title class="headline">{{ $t('common.deleteConfirmTitle') }}</v-card-title>

        <v-card-text>
          {{ $t('common.deleteConfirmText') }}.
        </v-card-text>

        <v-card-actions>
          <v-spacer/>
          <v-btn @click="deleteArmDialog = false" color="gray" text>
            {{ $t('common.keep') }}
          </v-btn>
          <v-btn @click="handleDeleteFilter" color="red" text>
            {{ $t('common.delete') }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script>
  import { mapActions, mapGetters, mapMutations, mapState } from 'vuex'
  import FormInput from '~/components/partials/FormInput'
  import FormSelect from '~/components/partials/FormSelect'

  export default {
    name: 'ArmSelector',
    components: { FormInput, FormSelect },
    computed: {
      ...mapGetters({
        armOptionList: 'arms/armOptionList'
      }),
      ...mapState({
        arm: state => state.arms.arm,
        armList: state => state.arms.armList
      })
    },
    data: () => ({
      armDialog: false,
      deleteArmDialog: false,
    }),
    methods: {
      ...mapActions({
        createArm: 'arms/createArm',
        deleteArm: 'arms/deleteArm',
        getArmList: 'arms/getArmList',
        getVisitList: 'visits/getVisitList',
        updateArm: 'arms/updateArm'
      }),
      ...mapMutations({
        clearArm: 'arms/clearArm',
        setArm: 'arms/setArm',
        updateArmField: 'arms/updateArmField'
      }),
      handleAddArm() {
        this.clearArm()
        this.armDialog = true
      },
      async handleSaveArm() {
        try {
          this.arm.id ? await this.updateArm() : await this.createArm()
          this.getArmList()
          this.getVisitList()
          this.armDialog = false
        } catch (e) {
          this.$toast.error(e.message)
        }
      },
      handleChangeArm(armId) {
        this.setArm(this.armList.filter(a => a.id === parseInt(armId))[0])
        this.getVisitList()
      },
      async handleDeleteFilter() {
        this.deleteArmDialog = false

        if (!this.arm.id) return

        await this.deleteArm(this.arm.id)
        await this.getArmList()
        this.selectFirstArm()
      },
      selectFirstArm() {
        if (this.armList.length) {
          this.setArm(this.armList[0])
          this.getVisitList()
        }
      }
    },
    created() {
      this.selectFirstArm()
    }
  }
</script>

<style scoped>

</style>
