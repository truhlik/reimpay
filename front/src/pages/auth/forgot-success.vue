<template>
  <div>
    <div class="h-100 bg-reimpay bg-animation">
      <div class="d-flex h-100 justify-content-center align-items-center">
        <v-col md="8" class="mx-auto app-login-box">
          <div class="app-logo-inverse mx-auto mb-3"/>
          <div class="modal-dialog mx-auto w-100">
            <div class="modal-content">
              <img src="~/assets/img/logos/color_wide.png" class="logo" alt="-">
              <div class="modal-body">
                <div class="divider"/>
                <p class="text-center font-size-xlg py-4">
                  {{ $t('auth.resetSuccess') }}<br/><br/>
                  {{ $t('auth.resetSuccess2') }}
                </p>
              </div>
              <div class="modal-footer d-block text-center">
                <nuxt-link :to="localePath({ name:'auth-login' })">
                  <v-btn
                    class="btn-shine"
                    color="primary"
                    size="lg"
                    type="submit"
                  >
                    {{ $t('auth.backToLogin') }}
                  </v-btn>
                </nuxt-link>
              </div>
            </div>
          </div>
          <div class="text-center text-white opacity-8 mt-3">
            {{ $t('common.copyright') }} &copy; {{ $t('common.reimpay') }} {{ now }}
          </div>
        </v-col>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'registerSuccess',
    layout: 'userpage',
    auth: false,
    data() {
      return {
        now: new Date().getFullYear(),
      }
    }
  }
</script>

<style scoped>
  .modal-body {
    padding: 0;
  }
</style>

