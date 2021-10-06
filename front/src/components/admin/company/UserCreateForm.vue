<template>
  <v-row>
    <FormInput
      :label="$t('auth.firstName')" :value="user.first_name" @input="updateField($event)" field="first_name"
      :breakpoints="{lg: 3, xl: 2}" required
    />

    <FormInput
      :label="$t('auth.lastName')" :value="user.last_name" @input="updateField($event)" field="last_name"
      :breakpoints="{lg: 3, xl: 2}" required
    />

    <FormInput
      :label="$t('auth.email')" :value="user.email" @input="updateField($event)" field="email" type="email"
      :breakpoints="{lg: 3, xl: 2}" required
    />

    <v-col :sm="6" :lg="3" class="py-0">
      <v-btn
        :color="isValid ? 'primary' : 'error'"
        :disabled="!isValid"
        size="lg"
        style="margin-top: 2px"
        @click="handleCreateUser"
      >
        {{ $t('common.save') }}
      </v-btn>
    </v-col>
  </v-row>
</template>

<script>
  import {mapActions} from 'vuex'
  import FormInput from "~/components/partials/FormInput"

  export default {
    name: "UserCreateForm",
    components: { FormInput },
    props: {
      role: {
        type: String,
        required: true
      }
    },
    computed: {
      isValid() {
        return this.user.first_name && this.user.last_name && this.user.email
      }
    },
    data: () => ({
        user: {
          first_name: '',
          last_name: '',
          email: ''
        }
      }),
    methods: {
      ...mapActions({
        createUser: 'company/createUser',
        getUserList: 'company/getUserList',
      }),
      handleCreateUser() {
        this.createUser({
          ...this.user,
          role: this.role
        }).then(
          () => {
            this.getUserList();
            this.$emit('saved');
          }
        )
      },
      updateField(updateObject) {
        this.user[updateObject.field] = updateObject.value;
      }
    }
  }
</script>

<style scoped>

</style>
