<template>
  <div>
    <div class="h-100 bg-reimpay bg-animation">
      <div class="d-flex h-100 justify-content-center align-items-center">
        <v-col md="6" class="mx-auto app-login-box">
          <div class="app-logo-inverse mx-auto mb-3"/>
          <div class="modal-dialog mx-auto w-100">
            <div class="modal-content">
              <img src="~/assets/img/logos/color_wide.png" class="logo" alt="logo">
              <div class="modal-header">
                <div class="h5 modal-title">
                  {{ $t('auth.forgottenPassword') }}
                  <h6 class="mt-1 mb-0 opacity-8">
                    <span>{{ $t('auth.forgottenPasswordHint') }}</span>
                  </h6>
                </div>
              </div>
              <div class="modal-body">
                <v-row>
                  <FormInput
                    :breakpoints="{sm: 12, md: 12, lg: 12, xl: 12}"
                    :label="$t('auth.email')"
                    :value="email"
                    @input="email = $event.value"
                    field="email"
                  />
                </v-row>
                <div class="divider"/>
                <h6 class="mb-0">
                  <nuxt-link :to="localePath({name:'auth-login'})" class="text-primary">
                    {{ $t('auth.signInExAcc') }}
                  </nuxt-link>
                </h6>
              </div>
              <div class="modal-footer clearfix">
                <div class="float-right">
                  <v-btn color="primary" size="lg" @click="sendResetRequest()" :disabled="!email">
                    {{ $t('auth.recoverPassword') }}
                  </v-btn>
                </div>
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
  import { AccountsService } from '~/service/api'

  export default {
    name: 'Forgot',
    layout: 'userpage',
    components: { FormInput },
    auth: false,
    data() {
      return {
        email: '',
        now: new Date().getFullYear()
      }
    },
    methods: {
      sendResetRequest() {
        AccountsService.accountsPasswordResetCreate({
          data: {
            email: this.email
          }
        }).then(
          () => this.$router.push(this.localePath({name:'auth-forgot-success'}))
        ).catch(
          err => this.$toast.error(err.detail)
        )
      }
    },
    head() {
      return {
        title: 'Forgotten password'
      }
    }
  }
</script>
