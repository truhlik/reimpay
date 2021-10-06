import { createNamespacedHelpers } from 'vuex'
import { DefineActions, DefineGetters, DefineMutations } from 'vuex-type-helper'

import {
  AuditLog, HistoryService
} from '~/service/api'


export interface State {
  historyList: AuditLog[]
  historyPagination: { page: number, page_size: number }   // a další atributy z backendu, které nemutujeme
}

export interface Getters {}

export interface Actions {
  getHistory: void
}

export interface Mutations {
  setHistory: any
  setHistoryPaginationPage: number
  setHistoryPaginationSize: number
}

export function state() {
  let state: State = {
    historyList: [],
    historyPagination: {
      page: 1,
      page_size: 50
    }
  }
  return state
}

export const getters: DefineGetters<Getters, State> = {
  // historyList: state => state.patientVisitItemList.filter(f => f.approved === true || f.approved === false),
}

export const actions: DefineActions<Actions, State, Mutations, Getters> = {

  async getHistory({commit, rootState}) {
    await HistoryService.historyList({
      page: rootState.history.historyPagination.page,
      pageSize: rootState.history.historyPagination.page_size,
      studyId: rootState.studies.study.id
    }).then(res => commit('setHistory', res))
  },
}

export const mutations: DefineMutations<Mutations, State> = {

  setHistory(state, responseData) {
    state.historyList = responseData.results
    state.historyPagination = responseData.pagination
  },

  setHistoryPaginationPage(state, pageNumber) {
    state.historyPagination.page = pageNumber
  },

  setHistoryPaginationSize(state, pageSize) {
    state.historyPagination.page_size = pageSize
  },
}

export const {
  mapState,
  mapGetters,
  mapMutations,
  mapActions,
} = createNamespacedHelpers<State, Getters, Mutations, Actions>('historyModule')

export const historyModule = {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
}
