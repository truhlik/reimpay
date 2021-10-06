import { createNamespacedHelpers } from 'vuex'
import { DefineActions, DefineGetters, DefineMutations } from 'vuex-type-helper'

import {
  AccountsService, User,
} from "~/service/api"

export interface State {
  user: User | Object
}

export interface Actions {
  getUser: void
}

export interface Mutations {
  setUser: User
}

export interface Getters {
  isAdmin: Boolean
}


export function state() {
  let state: State = {
    user: {}
  }
  return state
}

export const getters: DefineGetters<Getters, State> = {
  isAdmin: state => (state.user as any).role === 'ADMIN'
}

export const actions: DefineActions<Actions, State, Mutations, Getters> = {

  async getUser({commit, rootState}) {
    await AccountsService.accountsUserRead()
      .then(res => commit('setUser', res)
    )
  },

}

export const mutations: DefineMutations<Mutations, State> = {

  setUser(state, user) {
    state.user = user
  }

}

export const {
  mapState,
  mapGetters,
  mapMutations,
  mapActions,
} = createNamespacedHelpers<State, Getters, Mutations, Actions>('account')

export const account = {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
}
