import { createNamespacedHelpers } from 'vuex'
import { DefineActions, DefineGetters, DefineMutations } from 'vuex-type-helper'

import {
  TicketsService, Ticket
} from '~/service/api'


export interface State {}

export interface Getters {}

export interface Actions {
  createTicket: Ticket
}

export interface Mutations {}

export function state() {
  return {}
}

export const getters: DefineGetters<Getters, State> = {}

export const actions: DefineActions<Actions, State, Mutations, Getters> = {
  async createTicket({commit}, ticketData: Ticket) {
    await TicketsService.ticketsCreate({
      data: ticketData
    })
  },
}

export const mutations: DefineMutations<Mutations, State> = {}

export const {
  mapState,
  mapGetters,
  mapMutations,
  mapActions,
} = createNamespacedHelpers<State, Getters, Mutations, Actions>('tickets')

export const tickets = {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
}
