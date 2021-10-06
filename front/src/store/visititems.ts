import { createNamespacedHelpers } from 'vuex'
import { DefineActions, DefineGetters, DefineMutations } from 'vuex-type-helper'

import {
  VisitItemsService, VisitItem
} from '~/service/api'


export interface State {
  visitItemList: VisitItem[]
}

export interface Actions {
  createVisitItem: VisitItem
  getVisitItemList: string
  updateVisitItem: VisitItem
}

export interface Mutations {
  setVisitItemList: VisitItem[]
}

export interface Getters {
  visitItemOptionList: Object[]
}


export function state() {
  let state: State = {
    visitItemList: []
  }
  return state
}

export const getters: DefineGetters<Getters, State> = {
  visitItemOptionList: state => state.visitItemList.map(vi => ({value: vi.id, text: vi.study_item_obj.title}))
}

export const actions: DefineActions<Actions, State, Mutations, Getters> = {

  async createVisitItem({commit}, visitItem) {
    await VisitItemsService.visitItemsCreate({
      data: visitItem
    })
  },

  async getVisitItemList({commit, rootState}, visitId) {
    await VisitItemsService.visitItemsList({
      visitId: visitId || rootState.visits.visit.id
    }).then(res => commit('setVisitItemList', res.results)
    )
  },

  async updateVisitItem({commit}, visitItem) {
    await VisitItemsService.visitItemsUpdate({
      data: visitItem,
      id: visitItem.id
    })
  },
}

export const mutations: DefineMutations<Mutations, State> = {

  setVisitItemList(state, visitItemList) {
    state.visitItemList = visitItemList
  },
}

export const {
  mapState,
  mapGetters,
  mapMutations,
  mapActions,
} = createNamespacedHelpers<State, Getters, Mutations, Actions>('visits')

export const visits = {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
}
