<template>
  <div>
    <PageTitle :heading="title" :icon=icon :subheading=subheading />
    <v-card class="main-card">
      <v-card-text>
        <h5 class="text-uppercase mb-4">
          {{ $t('users.admins') }}
        </h5>
        <v-data-table
          :headers="tableHeaders"
          :items="userAdminList"
        >
          <template v-slot:item.id="{ item }">
            <v-btn @click="openDeleteDialog(item)" color="red" small>
              <v-icon color="white" small>delete</v-icon>
            </v-btn>
          </template>
        </v-data-table>

        <v-btn color="primary" v-if="!addingAdmin" @click="addingAdmin = true">
          {{ $t('users.addAdmin') }}
        </v-btn>

        <UserCreateForm :role="enumUserRole['ADMIN']" @saved="addingAdmin = false" v-else/>

        <hr class="m-5">

        <h5 class="text-uppercase">
          {{ $t('users.cras') }}
        </h5>
        <v-data-table
          :headers="tableHeaders"
          :items="userCraList"
        >
          <template v-slot:item.id="{ item }">
            <v-btn @click="openDeleteDialog(item)" color="red" small>
              <v-icon color="white" small>delete</v-icon>
            </v-btn>
          </template>
        </v-data-table>

        <v-btn color="primary" v-if="!addingCra" @click="addingCra = true">
          {{ $t('users.addCra') }}
        </v-btn>

        <UserCreateForm :role="enumUserRole['CRA']" @saved="addingCra = false" v-else/>
      </v-card-text>
    </v-card>

    <v-dialog max-width="480px" v-model="userDeleteDialog">
      <v-card>
        <v-card-title class="headline">
          {{ $t('users.deleteUser') }}
          {{ userToDelete ? `${userToDelete.first_name} ${userToDelete.last_name}` : '' }}?
        </v-card-title>
        <v-card-text>{{ $t('users.reallyDelete') }}</v-card-text>
        <v-card-actions>
          <v-spacer/>
          <v-btn @click="userDeleteDialog = false" color="gray" text>{{ $t('common.keep') }}</v-btn>
          <v-btn @click="handleDeleteUser" color="red" text>{{ $t('common.delete') }}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
  import {mapActions, mapGetters, mapState} from 'vuex';
  import PageTitle from '~/components/partials/PageTitle';
  import UserCreateForm from '~/components/admin/company/UserCreateForm';

  import { EnumUserRole } from '~/service/api';

  export default {
    name: 'user',
    components: {PageTitle, UserCreateForm},
    async fetch({store}) {
      await store.dispatch('company/getUserList');
    },
    computed: {
      ...mapState({
        userList: state => state.company.userList,
      }),
      ...mapGetters({
        userAdminList: 'company/userAdminList',
        userCraList: 'company/userCraList'
      }),
      tableHeaders() {
        return [
          { value: 'first_name', text: this.$t('auth.firstName') },
          { value: 'last_name', text: this.$t('auth.lastName') },
          { value: 'email', text: this.$t('auth.email') },
          { value: 'id', text: '' }
        ]
      }
    },
    data() {
      return {
        title: this.$t('users.title'),
        subheading: this.$t('users.subtitle'),
        icon: 'pe-7s-users icon-gradient bg-reimpay',

        addingAdmin: false,
        addingCra: false,

        enumUserRole: EnumUserRole,

        userDeleteDialog: false,
        userToDelete: null
      }
    },
    methods: {
      ...mapActions({
        deleteUser: 'company/deleteUser',
        getUserList: 'company/getUserList'
      }),
      async handleDeleteUser() {
        try {
          await this.deleteUser(this.userToDelete.id)
          this.$toast.success(this.$t('common.deletedSuccessfully'))
          this.userDeleteDialog = false
          this.getUserList()
        } catch (e) {
          this.$toast.error(e.message)
        }
      },
      openDeleteDialog(user) {
        this.userToDelete = user
        this.userDeleteDialog = true
      }
    }
  }
</script>
