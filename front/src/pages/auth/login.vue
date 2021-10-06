<template>
  <div>
    <div class="h-100 bg-reimpay bg-animation">
      <div class="d-flex h-100 justify-content-center align-items-center">
        <v-col md="8" class="mx-auto app-login-box">
          <div class="app-logo-inverse mx-auto mb-3"/>
          <div class="modal-dialog w-100 mx-auto">
            <div class="modal-content">
              <img src="~/assets/img/logos/color_wide.png" class="logo">
              <div class="modal-header">
                <div class="h5 modal-title">
                  {{ $t('auth.login') }}
                  <h6 class="mt-1 mb-0 opacity-8">
                    <span>{{ $t('auth.loginText') }}</span>
                  </h6>
                </div>
              </div>
              <div class="modal-body">
                <v-row>
                  <FormInput
                    :breakpoints="{sm: 12, md: 12, lg: 12, xl: 12}"
                    :value="email"
                    :label="$t('auth.email')"
                    @input="email = $event.value"
                    field="email"
                  />
                  <FormInput
                    :breakpoints="{sm: 12, md: 12, lg: 12, xl: 12}"
                    :label="$t('auth.password')"
                    :value="password"
                    @input="password = $event.value"
                    field="password"
                    type="password"
                  />
                </v-row>
                <div class="divider"/>
                <h6 class="mb-0">
                  <nuxt-link :to="localePath({name:'auth-forgot'})" class="text-primary">
                    {{ $t('auth.forgottenPassword') }}
                  </nuxt-link>
                </h6>
              </div>
              <div class="modal-footer d-block text-center">
                <v-btn
                  class="btn-shine"
                  color="primary"
                  :disabled="!email || !password"
                  size="lg"
                  type="submit"
                  @click="login"
                >
                  {{ $t('auth.login') }}
                </v-btn>
              </div>
            </div>
          </div>

          <div class="text-center text-white opacity-8 mt-3">
            {{ $t('common.copyright') }}&copy; {{ $t('common.reimpay') }} {{ now }}
          </div>
        </v-col>
      </div>
    </div>
  </div>
</template>

<script>
  import FormInput from '~/components/partials/FormInput'

  export default {
    name: 'Login',
    layout: 'userpage',
    components: { FormInput },
    data() {
      return {
        now: new Date().getFullYear(),
        password: '',
        email: '',
      }
    },
    methods: {
      login() {
        this.$auth.loginWith(
          'local', { data: { username: this.email, email: this.email, password: this.password }}
        ).then(
          res => this.$toast.success(this.$t('auth.loginSuccess')),
          err => this.$toast.error(this.$t('auth.loginFailure'))
        )
      }
    },
    head() {
      return {
        title: 'Login'
      }
    }
  }
</script>
