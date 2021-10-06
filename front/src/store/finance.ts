import { createNamespacedHelpers } from 'vuex'
import { DefineActions, DefineGetters, DefineMutations } from 'vuex-type-helper'
import FileSaver from 'file-saver'

import {
  CreditBalance, CreditInfo, CreditService, FinanceService, StudyStat
} from '~/service/api'


export interface State {
  creditInfo: CreditInfo
  creditList: CreditBalance[]
  stats: StudyStat
}

export interface Getters {}

export interface Actions {
  getCreditInfo: void
  getCreditList: void
  getCreditListExport: { createdAtDateGte: string, createdAtDateLte: string }
  getStats: void
}

export interface Mutations {
  setCreditInfo: CreditInfo
  setCreditList: CreditBalance[]
  setStats: StudyStat
}

export function state() {
  let state: State = {
    creditInfo: new CreditInfo(),
    creditList: [],
    stats: new StudyStat()
  }
  return state
}

export const getters: DefineGetters<Getters, State> = {}

export const actions: DefineActions<Actions, State, Mutations, Getters> = {

  async getCreditInfo({commit, rootState}) {
    await FinanceService.financeRead({
      id: rootState.studies.study.id
    }).then(res => commit('setCreditInfo', res))
  },

  async getCreditList({commit, rootState}) {
    await CreditService.creditList({
      pageSize: 9999,
      studyId: rootState.studies.study.id
    }).then(res => commit('setCreditList', res.results))
  },

  async getCreditListExport({commit, rootState}, exportFilter) {
    const response = await CreditService.creditExport({
      ...exportFilter,
      pageSize: 9999,
    }, {
      responseType: 'blob'
    })

    FileSaver.saveAs(response, 'creditBalanceExport.csv')
  },

  async getStats({commit, rootState}) {
    await FinanceService.financeStats({
      id: rootState.studies.study.id
    }).then(res => commit('setStats', res))
  },
}

export const mutations: DefineMutations<Mutations, State> = {

  setCreditInfo(state, creditInfo) {
    state.creditInfo = creditInfo
  },

  setCreditList(state, creditList) {
    state.creditList = creditList
  },

  setStats(state, stats) {
    state.stats = stats
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
