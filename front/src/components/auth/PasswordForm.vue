<template>
  <v-row>
    <v-col md="6">
      <v-text-field
        :placeholder="`${$t('auth.enterPassword')}...`"
        required=""
        :type="password"
        v-model="user.password1"
      />
    </v-col>
    <v-col md="6">
      <v-text-field
        :placeholder="`${$t('auth.repeatPassword')}...`"
        required=""
        :type="password"
        v-model="user.password2"
      />
    </v-col>
  </v-row>
</template>

<script>
  // TODO
  // import { validatePassword, validatePasswordConfirm } from "~/helpers/validators";

  export default {
    name: "PasswordForm",
    props: {
      user: {
        type: Object,
        required: true,
      }
    },
    data() {
      return {
        isCompany: false,
      }
    },
    methods: {
      // checkValidity() {
      //   const validator = this.getValidator();
      //   for (let key in validator)
      //     if(validator[key].valid === false) {
      //       this.$emit('validationChange', false);
      //       return;
      //     }
      //
      //   this.$emit('validationChange', true);
      // },
      // getValidator() {
      //   return  {
      //     password: validatePassword(this.user.password),
      //     password_confirmation: validatePasswordConfirm(this.user.password_confirmation, this.user.password)
      //   };
      // },
    }
  }
</script>

<style scoped>

</style>
