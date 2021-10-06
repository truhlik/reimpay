<template>
  <div class="d-flex" v-if="loggedIn">
    <div class="header-btn-lg pr-0">
      <div class="widget-content p-0">
        <div class="widget-content-wrapper">
          <div class="widget-content-left d-flex align-items-center">
            <strong class="color-brand display-inline-block mr-3">
              {{ user.first_name }} {{ user.last_name }}
            </strong>

            <v-menu offset-y>
              <template v-slot:activator="{ on }">
                <div slot="button-content" v-on="on">
                  <div class="icon-wrapper icon-wrapper-alt rounded-circle">
                    <i class="pe-7s-user"/>
                    <v-icon>mdi-chevron-down</v-icon>
                  </div>
                </div>
              </template>
              <div class="bg-reimpay p-3 d-flex flex-column">
                <nuxt-link :to="localePath({name:'auth-change-pass'})" class="text-decoration-none">
                  <v-btn class="mb-2">
                    {{ $t('auth.changePassword') }}
                  </v-btn>
                </nuxt-link>
                <v-btn @click="logout" color="error">
                  {{ $t('auth.logout') }}
                </v-btn>
              </div>
            </v-menu>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

  export default {
    props: {
      loggedIn: Boolean,
      user: Object,
    },
    methods: {
      async logout() {
        await this.$auth.logout();
      }
    }
  }
</script>

<style lang="scss">
  .dropdown-menu {
    padding: 0;

    & > .dropdown-menu-header {
      margin: 0;
    }
  }

  .icon-wrapper {
    align-items: center;
    display: flex;
    font-size: 1.5rem;

    i {
      font-size: 2rem;
    }
  }
</style>
