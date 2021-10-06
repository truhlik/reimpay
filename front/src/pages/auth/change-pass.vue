<template>
  <div>
    <PageTitle :heading=title :subheading=subheading :icon=icon />
    <v-card :title="title" class="main-card mb-4">
      <v-card-text>
        <v-row class="mb-4">
          <FormInput
            type="password" :label="$t('auth.newPassword')" :value="password" required
            @change="password = $event.value"
          />
          <FormInput
            type="password" :label="$t('auth.repeatPassword')" :value="password_confirmation" required
            @change="password_confirmation = $event.value"
          />
        </v-row>

        <v-row>
          <v-col cols="12" class="mt-2 text-center">
            <v-btn class="btn-shadow" color="primary" size="lg" @click="changePassword(password, password_confirmation)">
              {{ $t('auth.changePassword') }}
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
  import PasswordForm from '~/components/auth/PasswordForm'
  import FormInput from '~/components/partials/FormInput'
  import PageTitle from '~/components/partials/PageTitle'
  import { validatePassword, validatePasswordConfirm } from '~/helpers/validators'
  import { AccountsService } from '~/service/api.ts'

  export default {
    name: 'passwordChange',
    components: { FormInput, PageTitle, PasswordForm },
    data() {
      return {
        title: this.$t('passwordChange.title'),
        subheading: this.$t('passwordChange.subtitle'),
        icon: 'pe-7s-key icon-gradient bg-reimpay',

        formValid: false,
        old_password: undefined,
        password: undefined,
        password_confirmation: undefined,

        validator: {
          password: {},
          password_confirmation: {}
        }
      }
    },
    methods: {
      changePassword(){
        AccountsService.accountsPasswordChangeCreate({
          data: {
            new_password1: this.password,
            new_password2: this.password_confirmation,
          }
         }).then(
          (res) => {
            this.$toast.success(res.detail)
            this.clearForm()
          },
          err => this.$toast.error(err)
        )
      },
      checkValidity() {
        for (let key in this.validator)
          if(this.validator[key].valid === false) {
            this.formValid = false
            return
          }

        this.formValid = true
      },
      clearForm() {
        this.old_password = undefined
        this.password = undefined
        this.password_confirmation = undefined
        this.setValidator()
      },
      setValidator() {
        this.validator = {
          password: validatePassword(this.password),
          password_confirmation: validatePasswordConfirm(this.password_confirmation, this.password)
        }
      },
    },
    mounted() {
      if (!this.$auth.loggedIn)
        this.$router.push(this.localePath({name: 'auth-login'}))

      this.setValidator()
    }
  }
</script>

<style scoped>
  :disabled {
    cursor: not-allowed;
  }
</style>

