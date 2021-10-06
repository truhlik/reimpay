<template>
  <v-row>
    <v-col md="6" lg="4">
      <table>
        <tr>
          <th class="pb-3">{{ $t('common.company') }}</th>
          <td class="pb-3">
            {{ company.name }}
          </td>
        </tr>
        <tr/>
        <tr v-if="company.street || company.street_number ">
          <th>{{ $t('location.street') }}</th>
          <td>{{ company.street }} {{ company.street_number }}</td>
        </tr>
        <tr v-if="company.city">
          <th>{{ $t('location.city') }}</th>
          <td>{{ company.city }}</td>
        </tr>
        <tr v-if="company.zip">
          <th>{{ $t('location.zip') }}</th>
          <td>{{ company.zip }}</td>
        </tr>
        <tr v-if="company.reg_number">
          <th>{{ $t('company.id') }}</th>
          <td>{{ company.reg_number }}</td>
        </tr>
        <tr v-if="company.vat_number">
          <th>{{ $t('company.vatId') }}</th>
          <td>{{ company.vat_number }}</td>
        </tr>
        <tr/>
        <tr v-if="company.iban">
          <th>{{ $t('company.iban') }}</th>
          <td>{{ company.iban }}</td>
        </tr>
        <tr v-if="company.phone">
          <th>{{ $t('company.phone') }}</th>
          <td>{{ company.phone }}</td>
        </tr>
        <tr v-if="company.email">
          <th>{{ $t('company.email') }}</th>
          <td>{{ company.email }}</td>
        </tr>
        <tr v-if="company.web">
          <th>{{ $t('company.web') }}</th>
          <td>{{ company.web }}</td>
        </tr>
      </table>
    </v-col>
  </v-row>
</template>

<script>
  import {mapState} from "vuex";

  export default {
    name: "CompanySummary",
    computed: {
      ...mapState({
        company: state => state.company.company,
      })
    },
  }
</script>

<style lang="scss" scoped>
  table {
    font-size: 18px;
    line-height: 1.2;
    text-align: left;
    width: 100%;

    th, td {
      padding: 0.75rem 2rem;
    }
  }
</style>
