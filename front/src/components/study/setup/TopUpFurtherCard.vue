<template>
  <div class="color-secondary d-flex align-items-center justify-content-between w-100">
    <span class="font-size-lg">{{ item.label }}</span>
    <v-spacer/>
    <span class="d-inline-flex justify-content-end" style="max-width: 120px">
      <v-btn
        color="primary"
        :disabled="!item.enabled"
        v-if="!item.completed"
        @click="topUpDialog = true"
      >
        {{ item.slug }}
      </v-btn>
      <v-icon color="green" v-else>check</v-icon>
    </span>
    <v-dialog max-width="600" v-model="topUpDialog">
      <TopUpRequestForm @sent="topUpDialog = false"/>
    </v-dialog>
  </div>
</template>

<script>
  import TopUpRequestForm from '~/components/study/finance/TopUpRequestForm'

  export default {
    name: 'TopUpFurtherCard',
    components: { TopUpRequestForm },
    props: {
      item: {
        type: Object,
        required: true
      }
    },
    data: () => ({
      topUpDialog: false
    })
  }
</script>

<style scoped>

</style>
