<template>
  <v-card class="main-card">
    <v-card-text>
      <v-data-table
        :headers="tableHeaders"
        :items="studyItemList"
      >
        <template v-slot:item.id="{ item }">
          <v-btn @click="handleDeleteStudyItem(item.id)" color="red" small>
            <v-icon color="white" small>delete</v-icon>
          </v-btn>
        </template>
      </v-data-table>

      <v-btn @click="addingItem = true" color="primary" v-if="!addingItem">
        {{ $t('studies.reims.addItem') }}
      </v-btn>

      <StudyItemCreateForm @saved="addingItem = false" v-else/>
    </v-card-text>
  </v-card>
</template>

<script>
  import {mapActions, mapState} from "vuex";
  import StudyItemCreateForm from "~/components/study/reims/StudyItemCreateForm";

  export default {
    name: 'SetupItems',
    components: { StudyItemCreateForm },
    computed: {
      ...mapState({
        studyItemList: state => state.studyitems.studyItemList,
      }),
      tableHeaders() {
        return [
          { value: 'title', text: this.$t('common.englishTitle') },
          { value: 'description', text: this.$t('common.localTitleVisible') },
          { value: 'price', text: this.$t('common.price') },
          { value: 'id', text: '' }
        ]
      }
    },
    data() {
      return {
        addingItem: false
      }
    },
    methods: {
      ...mapActions({
        deleteStudyItem: 'studyitems/deleteStudyItem',
        getStudyItemList: 'studyitems/getStudyItemList'
      }),
      async handleDeleteStudyItem(itemId) {
        try {
          await this.deleteStudyItem(itemId)
          this.getStudyItemList()
        } catch (e) {
          this.$toast.error(e.message)
        }
      }
    },
    created() {
      this.getStudyItemList();
    }
  }
</script>

<style scoped>

</style>
