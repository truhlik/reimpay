<template>
  <v-card class="mb-5">
    <v-card-text
      :class="`d-flex flex-wrap flex-column flex-sm-row justify-content-${isAdmin ? 'around' : 'start'} p-2 w-100`"
      style="overflow: auto"
    >
      <nuxt-link
        :to="item.route"
        :class="`d-flex align-items-center text-decoration-none}} ${item.active ? 'background-primary' : ''}`"
        :key="`route-${index}`"
        v-for="(item, index) in menuItems"
        v-if="item.unrestricted || isAdmin"
      >
        <v-btn :color="item.active ? 'white' : undefined" :disabled="item.disabled" class="hover-color-primary" large text>
          {{ item.text }}
        </v-btn>
      </nuxt-link>
    </v-card-text>
  </v-card>
</template>

<script>
  import { mapGetters } from 'vuex'

  export default {
    name: "StudyMenu",
    props: {
      isNew: {
        type: Boolean,
        default: false,
      },
      studyId: {
        type: String,
        required: false
      },
      activeItem: {
        type: String,
        required: true
      }
    },
    computed: {
      ...mapGetters({
        isAdmin: 'account/isAdmin'
      }),
      menuItems: function () {
        return [
          {
            active: this.activeItem === 'setup',
            disabled: false,
            route: this.localePath(
              this.isNew ? {name: 'studies-new-setup'} : {name: 'studies-id-setup', params: {id: this.studyId}}
            ),
            text: this.$t('studies.menu.setup'),
            unrestricted: false
          },
          {
            active: this.activeItem === 'general',
            disabled: false,
            route: this.localePath(
              this.isNew ? {name: 'studies-new-general'} : {name: 'studies-id-general', params: {id: this.studyId}}
            ),
            text: this.$t('studies.menu.general'),
            unrestricted: false
          },
          {
            active: this.activeItem === 'reims',
            disabled: !this.studyId,
            route: this.localePath(
              this.isNew ? {name: 'studies-new-reims'} : {name: 'studies-id-reims', params: {id: this.studyId}}
            ),
            text: this.$t('studies.menu.reims'),
            unrestricted: false
          },
          {
            active: this.activeItem === 'visits',
            disabled: !this.studyId,
            route: this.localePath(
              this.isNew ? {name: 'studies-new-visits'} : {name: 'studies-id-visits', params: {id: this.studyId}}
            ),
            text: this.$t('studies.menu.visits'),
            unrestricted: false
          },
          {
            active: this.activeItem === 'sites',
            disabled: !this.studyId,
            route: this.localePath(
              this.isNew ? {name: 'studies-new-sites'} : {name: 'studies-id-sites', params: {id: this.studyId}}
            ),
            text: this.$t('studies.menu.sites'),
            unrestricted: false
          },
          {
            active: this.activeItem === 'patients',
            disabled: !this.studyId,
            route: this.localePath(
              this.isNew ? {name: 'studies-new-patients'} : {name: 'studies-id-patients', params: {id: this.studyId}}
            ),
            text: this.$t('studies.menu.patients'),
            unrestricted: true
          },
          {
            active: this.activeItem === 'approvals',
            disabled: !this.studyId,
            route: this.localePath(
              this.isNew ? {name: 'studies-new-approvals'} : {name: 'studies-id-approvals', params: {id: this.studyId}}
            ),
            text: this.$t('studies.menu.approvals'),
            unrestricted: true
          },
          {
            active: this.activeItem === 'finance',
            disabled: !this.studyId,
            route: this.localePath(
              this.isNew ? {name: 'studies-new-finance'} : {name: 'studies-id-finance', params: {id: this.studyId}}
            ),
            text: this.$t('studies.menu.finance'),
            unrestricted: false
          },
          {
            active: this.activeItem === 'stats',
            disabled: !this.studyId,
            route: this.localePath(
              this.isNew ? {name: 'studies-new-stats'} : {name: 'studies-id-stats', params: {id: this.studyId}}
            ),
            text: this.$t('studies.menu.stats'),
            unrestricted: true
          },
          {
            active: this.activeItem === 'history',
            disabled: !this.studyId,
            route: this.localePath(
              this.isNew ? {name: 'studies-new-history'} : {name: 'studies-id-history', params: {id: this.studyId}}
            ),
            text: this.$t('studies.menu.history'),
            unrestricted: false
          },
        ]
      }
    }
  }
</script>

<style scoped>

</style>
