import { createNamespacedHelpers } from 'vuex'
import { DefineActions, DefineGetters, DefineMutations } from 'vuex-type-helper'

import {
  TopUp, TopupsService
} from '~/service/api'


export interface State {
  topUp: TopUp
  topUpList: TopUp[]
}

export interface Getters {}

export interface Actions {
  createTopUp: number
  getTopUpList: void
}

export interface Mutations {
  setTopUp: TopUp
  setTopUpList: TopUp[]
}

export function state() {
  let state: State = {
    topUp: new TopUp(),
    topUpList: []
  }
  return state
}

export const getters: DefineGetters<Getters, State> = {}

export const actions: DefineActions<Actions, State, Mutations, Getters> = {

  async createTopUp({commit, rootState}, amount) {
    const response = await TopupsService.topupsCreate({
      data: new TopUp({
        amount: amount,
        study: rootState.studies.study.id
      })
    })

    commit('setTopUp', response)
  },

  async getTopUpList({commit, rootState}) {
    const response = await TopupsService.topupsList({
      pageSize: 999,
      studyId: rootState.studies.study.id
    })

    commit('setTopUpList', response.results)
  },
}

export const mutations: DefineMutations<Mutations, State> = {

  setTopUp(state, topUp) {
    state.topUp = topUp
  },

  setTopUpList(state, topUpList) {
    state.topUpList = topUpList
  },
}

export const {
  mapState,
  mapGetters,
  mapMutations,
  mapActions,
} = createNamespacedHelpers<State, Getters, Mutations, Actions>('creditModule')

export const creditModule = {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
}
