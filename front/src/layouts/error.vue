<template>
  <div>
    <div class="h-100 bg-reimpay bg-animation">
      <div class="d-flex h-100 justify-content-center align-items-center">
        <v-col md="8" class="mx-auto app-login-box">
          <div class="modal-dialog w-100 mx-auto">
            <div class="modal-content">
              <div class="modal-body">
                <div class="h5 modal-title text-center">
                  <h1 v-if="error.statusCode === 404">{{ $t('common.pageError') }}</h1>
                  <h1 v-else>
                    {{ `${$t('common.pageErrorAnother')}...` }}
                    <br>
                    <small>{{ $t('common.letsHeadTo') }} <nuxt-link to="/">{{ $t('common.homepage') }}</nuxt-link>...</small>
                  </h1>
                </div>
                <div class="divider"/>
                <h6 class="mb-0 text-center">
                  <nuxt-link to="/">{{ $t('common.homepageDiv') }}</nuxt-link>
                </h6>
              </div>
            </div>
          </div>
        </v-col>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['error'],
  layout: 'userpage' // you can set a custom layout for the error page
}
</script>
