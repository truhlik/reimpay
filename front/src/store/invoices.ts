import { createNamespacedHelpers } from 'vuex'
import { DefineActions, DefineGetters, DefineMutations } from 'vuex-type-helper'

import {
  Invoice, InvoicesService
} from '~/service/api'


export interface State {
  invoiceList: Invoice[]
}

export interface Getters {}

export interface Actions {
  getInvoiceList: void
}

export interface Mutations {
  setInvoiceList: Invoice[]
}

export function state() {
  let state: State = {
    invoiceList: []
  }
  return state
}

export const getters: DefineGetters<Getters, State> = {}

export const actions: DefineActions<Actions, State, Mutations, Getters> = {
  async getInvoiceList({commit}) {
    await InvoicesService.invoicesList({
      pageSize: 999
    }).then(res => commit('setInvoiceList', res.results))
  },
}

export const mutations: DefineMutations<Mutations, State> = {
  setInvoiceList(state, invoiceList) {
    state.invoiceList = invoiceList
  },
}

export const {
  mapState,
  mapGetters,
  mapMutations,
  mapActions,
} = createNamespacedHelpers<State, Getters, Mutations, Actions>('invoices')

export const invoices = {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
}
