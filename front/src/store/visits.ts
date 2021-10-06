import { createNamespacedHelpers } from 'vuex'
import { DefineActions, DefineGetters, DefineMutations } from 'vuex-type-helper'

import {
  VisitsService, VisitItemsService, Visit, VisitItem
} from '~/service/api'


export interface State {
  loading: boolean,
  visit: Visit
  visitList: Visit[]
  visitPagination: { page: number, num_pages: number }
}

export interface Actions {
  createVisit: Visit
  createVisitItem: VisitItem      // todo USE ALL VISITITEMS from visititems.ts
  deleteVisit: number
  deleteVisitItem: number
  getVisit: number
  getVisitList: void
  partialUpdateVisit: Visit
  updateVisit: void
  updateVisitItem: VisitItem
}

export interface Mutations {
  setLoading: boolean
  setPaginationPage: number
  setVisit: Visit
  setVisitList: Visit[]
  setVisitPagination: { page: number, num_pages: number }
  updateVisitField: { field: string, value: string }
}

export interface Getters {
  lastRegularVisitId: number | null
  visitOptionList: Object[]
}


export function state() {
  let state: State = {
    loading: false,
    visit: new Visit(),
    visitList: [],
    visitPagination: { page: 1, num_pages: 1 }
  }
  return state
}

export const getters: DefineGetters<Getters, State> = {
  lastRegularVisitId: state => {
    const lastRegularVisit = state.visitList.filter(v => v.visit_type === 'REGULAR').slice(-1).pop()
    return lastRegularVisit ? lastRegularVisit.id : null
  },
  visitOptionList: state => state.visitList.map(v => ({value: v.id, text: v.title}))
}

export const actions: DefineActions<Actions, State, Mutations, Getters> = {

  async createVisit({commit, rootState}, visit) {
    await VisitsService.visitsCreate({
      data: {
        ...visit,
        arm: visit.arm || rootState.arms.arm.id
      }
    }).then(res => commit('setVisit', res))
  },

  async createVisitItem({commit}, visitItem) {
    await VisitItemsService.visitItemsCreate({
      data: visitItem
    })
  },

  async deleteVisit({commit, rootState}, visitId: number) {
    await VisitsService.visitsDelete({
      id: visitId
    })
  },

  async deleteVisitItem({commit, rootState}, visitItemId: number) {
    await VisitItemsService.visitItemsDelete({
      id: visitItemId
    })
  },

  async getVisit({commit}, visitId: number) {
    await VisitsService.visitsRead({
      id: visitId
    }).then(res => commit('setVisit', res)
    )
  },

  async getVisitList({commit, rootState}) {
    commit('setLoading', true)

    const response = await VisitsService.visitsList({
      armId: rootState.arms.arm.id || '',
      page: rootState.visits.visitPagination.page || 1,
      pageSize: 10,
      studyId: rootState.studies.study.id || ''
    })

    commit('setVisitList', response.results)
    commit('setVisitPagination', response.pagination)
    commit('setLoading', false)
  },

  async partialUpdateVisit({commit, rootState}, patchData) {
    await VisitsService.visitsPartialUpdate({
      data: patchData,
      id: patchData.id
    })
  },

  async updateVisit({commit, rootState}) {
    await VisitsService.visitsUpdate({
      data: rootState.visits.visit,
      id: rootState.visits.visit.id
    })
  },

  async updateVisitItem({commit}, visitItem) {
    await VisitItemsService.visitItemsUpdate({
      data: visitItem,
      id: visitItem.id
    })
  },
}

export const mutations: DefineMutations<Mutations, State> = {

  setLoading(state, isLoading) {
    state.loading = isLoading
  },

  setPaginationPage(state, pageNumber: number) {
    state.visitPagination.page = pageNumber
  },

  setVisit(state, visit: Visit) {
    state.visit = visit
  },

  setVisitList(state, visitList) {
    state.visitList = visitList
  },

  setVisitPagination(state, pagination) {
    state.visitPagination = pagination
  },

  updateVisitField(state, {field: field, value: value}) {
    (state.visit as any)[field] = value
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
