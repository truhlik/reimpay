<template>
  <div v-if="configPart" class="mb-10">
    <h5>{{ configPart.label }}</h5>
    <v-card :key="`${configPart.label}${index}`" class="mb-2" v-for="(item, index) of configPart.items">
<!--      <v-expansion-panel :disabled="!item.enabled" :key="`${configPart.label}${index}`" v-for="(item, index) of configPart.items">-->
      <v-card-text
        class="d-flex align-items-center"
        style="min-height: 68px"
      >
        <PrelaunchCard
          :item="item"
          v-if="item.slug === 'prelaunch'"
        />
        <TopUpCard
          :item="item"
          v-else-if="item.slug === 'topup' && configPart.label === 'Study setup'"
        />
        <TopUpFurtherCard
          :item="item"
          v-else-if="item.slug === 'topup' && configPart.label === 'Study in progress'"
        />
        <CloseStudyCard
          :item="item"
          v-else-if="item.slug === 'close'"
        />
        <nuxt-link
          class="color-secondary d-flex align-items-center justify-content-between w-100"
          :disabled="item.disabled ? '' : 'click'"
          :tag="item.disabled ? 'button' : 'a'"
          :to="localePath(study.id ? { name: `studies-id-${item.slug}`, params: {id: study.id}} : {name: `studies-new-${item.slug}` })"
          v-else
        >
          <span class="font-size-lg">{{ item.label }}</span>
          <v-spacer/>
          <span class="d-inline-flex justify-content-end" style="max-width: 120px">
            <v-btn
              color="primary"
              :disabled="!item.enabled"
              v-if="!item.completed"
              @click="$router.push(localePath(study.id ? {name: `studies-id-${item.slug}`, params: {id: study.id}} : {name: `studies-new-${item.slug}`}))"
            >
              {{ item.slug }}
            </v-btn>
            <v-icon color="green" v-else>check</v-icon>
          </span>
        </nuxt-link>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
  import { mapState } from 'vuex'
  import CloseStudyCard from '~/components/study/setup/CloseStudyCard'
  import PrelaunchCard from '~/components/study/setup/PrelaunchCard'
  import TopUpCard from '~/components/study/setup/TopUpCard'
  import TopUpFurtherCard from '~/components/study/setup/TopUpFurtherCard'

  export default {
    name: 'WizardBlock',
    components: { CloseStudyCard, PrelaunchCard, TopUpCard, TopUpFurtherCard },
    props: {
      configPart: {
        type: Object,
        required: true
      },
    },
    computed: {
      ...mapState({
        study: state => state.studies.study
      })
    }
  }
</script>

<style scoped>

</style>
