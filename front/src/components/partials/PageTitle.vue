<template>
  <div class="app-page-title">
    <div class="page-title-wrapper">
      <div class="page-title-heading">
        <div class="page-title-icon">
          <i :class="icon"/>
        </div>
        <div>
          {{ heading }}
          <span v-if="showStudyInfo && study">
            - {{ study.identifier }}
            <v-chip color="primary" small>{{ study.status }}</v-chip>
          </span>
          <div class="page-title-subheading">
            {{ subheading }}
          </div>
        </div>
      </div>
      <div class="page-title-actions" v-if="buttonText">
        <v-btn @click="$emit('btnClick')" color="primary" large>
          {{ buttonText }}
        </v-btn>
      </div>
    </div>
  </div>
</template>

<script>
  import { mapState } from 'vuex'

  export default {
    props: {
      icon: String,
      heading: String,
      subheading: String,
      buttonText: String,
      showStudyInfo: {
        type: Boolean,
        default: false
      }
    },
    computed: {
      ...mapState({
        study: state => state.studies.study
      })
    }
  }
</script>
