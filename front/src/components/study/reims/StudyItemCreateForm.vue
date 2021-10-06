<template>
  <v-row>
    <FormInput
      :breakpoints="{lg: 3, xl: 2}" :label="$t('common.englishTitle')" :value="studyItem.title"
      @input="updateStudyItemField($event)" field="title" required
    />

    <FormInput
      :breakpoints="{lg: 3, xl: 2}" :label="$t('common.localTitleVisible')" :value="studyItem.description"
      @input="updateStudyItemField($event)" field="description" required
    />

    <FormInput
      :breakpoints="{lg: 3, xl: 2}" :label="$t('common.price')" :value="studyItem.price"
      @input="updateStudyItemField($event)" field="price" required
      type="number"
      :rules="[
        value => !isNaN(value) && value > 0 || $t('errors.positiveNumber')
      ]"
    />

    <v-col :lg="3" :sm="6" class="py-0">
      <v-btn
        :color="isValid ? 'primary' : 'error'"
        :disabled="!isValid"
        @click="handleCreateStudyItem"
        size="lg"
        style="margin-top: 2px"
      >
        {{ $t('common.save') }}
      </v-btn>
    </v-col>
  </v-row>
</template>

<script>
  import { mapActions, mapMutations } from 'vuex'
  import FormInput from "~/components/partials/FormInput"

  export default {
    name: 'StudyItemCreateForm',
    components: { FormInput },
    computed: {
      isValid() {
        return this.studyItem.title && this.studyItem.description && this.studyItem.price
      }
    },
    data() {
      return {
        studyItem: {
          title: '',
          description: '',
          price: ''
        }
      }
    },
    methods: {
      ...mapActions({
        createStudyItem: 'studyitems/createStudyItem',
        getStudyItemList: 'studyitems/getStudyItemList'
      }),
      ...mapMutations({
        clearStudyItem: 'studyitems/clearStudyItem',
        // updateStudyItemField: 'studyitems/updateStudyItemField'
      }),
      handleCreateStudyItem() {
        this.createStudyItem({
          ...this.studyItem,
          study: this.$route.params.id
        }).then(
          () => {
            this.getStudyItemList();
            this.$emit('saved');
            this.clearStudyItem();
          }
        )
      },
      updateStudyItemField(updateObject) {
        this.studyItem[updateObject.field] = updateObject.value;
      }
    }
  }
</script>

<style scoped>

</style>
