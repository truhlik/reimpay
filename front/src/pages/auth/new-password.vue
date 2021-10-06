<template>
  <div>
    <div class="h-100 bg-reimpay bg-animation">
      <div class="d-flex h-100 justify-content-center align-items-center">
        <v-col md="8" class="mx-auto app-login-box">
          <div class="app-logo-inverse mx-auto mb-3"/>
          <div class="modal-dialog w-100 mx-auto">
            <div class="modal-content">
              <img src="~/assets/img/logos/color_wide.png" class="logo" alt="logo">
              <div class="modal-header">
                <div class="h5 modal-title">
                  {{ $t('auth.newPassword') }}
                  <h6 class="mt-1 mb-0 opacity-8">
                    <span>{{ $t('auth.newPasswordText') }}</span>
                  </h6>
                </div>
              </div>
              <div class="modal-body">
                <div>
                  <v-row form>

                    <FormInput
                      :breakpoints="{xs: 12}"
                      class="mb-2"
                      field="new_password1"
                      :hint="$t('auth.passwordHint')"
                      :label="$t('auth.newPassword')"
                      required
                      type="password"
                      :value="auth.new_password1"
                      @change="auth.new_password1 = $event.value"
                    />
                    <FormInput
                      :breakpoints="{xs: 12}"
                      field="new_password2"
                      :label="$t('auth.repeatPassword')"
                      required
                      type="password"
                      :value="auth.new_password2"
                      @change="auth.new_password2 = $event.value"
                    />
                  </v-row>
                </div>
              </div>
              <div class="modal-footer d-block text-center">
                <v-btn
                  color="primary"
                  class="btn-shine"
                  size="lg"
                  :disabled="!auth.new_password1 || auth.new_password1 !== auth.new_password2"
                  @click="sendNewPassword"
                >
                  {{ $t('common.save') }}
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
  import { mapState } from 'vuex'
  import FormInput from '~/components/partials/FormInput'
  import { AccountsService } from '~/service/api'

  export default {
    name: 'new-password',
    layout: 'userpage',
    auth: false,
    components: { FormInput },
    computed: {
      ...mapState({
        loggedIn: state => state.users.status,
      })
    },
    data() {
      const token = this.$route.query.token;
      const uid = this.$route.query.uid;

      return {
        now: new Date().getFullYear(),
        auth: {
          new_password1: '',
          new_password2: '',
          token: token,
          uid: uid
        },
      }
    },
    methods: {
      sendNewPassword() {
        AccountsService.accountsPasswordResetConfirmCreate({
          data: this.auth
        }).then(
          res => {
            this.$toast.success(this.$t('auth.newPasswordSuccess'));
            this.$router.push(this.localePath({name: 'auth-login'}));
          },
          err => this.$toast.error(this.$t('common.correctErrors'))
        )
      }
    },
    head() {
      return {
        title: this.$t('auth.newPassword')
      }
    }
  }
</script>
