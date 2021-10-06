<template>
  <v-card style="max-width: 800px">
    <v-card-title>
      {{ $t('contact.form') }}
    </v-card-title>
    <v-card-text>
      <v-row>
        <FormInput
          :label="$t('contact.subject')"
          :value="ticket.subject"
          @change="ticket.subject = $event.value"
        />
        <v-col cols="12">
          <v-textarea :label="$t('contact.text')" dense hide-details outlined v-model="ticket.text"/>
        </v-col>
      </v-row>
    </v-card-text>
    <v-card-actions class="justify-content-center pb-5">
      <v-btn @click="handleSend" color="primary" x-large>
        {{ $t('common.send') }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
  import {mapActions, mapState} from 'vuex'

  import FormInput from '~/components/partials/FormInput'

  export default {
    name: 'ContactForm',
    components: { FormInput },
    computed: {
      ...mapState({
        user: state => state.account.user
      })
    },
    data: () => ({
      ticket: {
        email: '',
        subject: '',
        text: ''
      }
    }),
    methods: {
      ...mapActions({
        createTicket: 'tickets/createTicket'
      }),
      handleSend() {
        try {
          this.createTicket(this.ticket)
          this.$emit('sent')
          this.$toast.success(this.$t('common.sentSuccessfully'))
        } catch (e) {
          this.$toast.error(e.message)
        }
      }
    },
    created() {
      this.ticket.email = this.user.email
    }
  }
</script>

<style scoped>

</style>
