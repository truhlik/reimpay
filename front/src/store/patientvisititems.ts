import { createNamespacedHelpers } from 'vuex'
import { DefineActions, DefineGetters, DefineMutations } from 'vuex-type-helper'

import {
  PatientVisitItemsService, PatientVisitItem
} from '~/service/api'


export interface State {
  patientVisitItemList: PatientVisitItem[]
  patientVisitItemHistoryList: PatientVisitItem[]
  patientVisitItemHistoryPagination: { page: number, page_size: number }   // a další atributy z backendu, které nemutujeme
  unapprovedItemsCount: number | null
}

export interface Actions {
  createPatientVisitItem: PatientVisitItem
  getPatientVisitItemList: void
  getPatientVisitItemHistoryList: object
  getUnapprovedItemsCount: void
  patchApproval: PatientVisitItem,    // just patch object, not whole type but required by TS
  returnReimsForPatientVisit: string
}

export interface Mutations {
  setPatientVisitItemList: PatientVisitItem[]
  setPatientVisitItemHistoryList: any
  setPatientVisitItemHistoryPaginationPage: number
  setPatientVisitItemHistoryPaginationSize: number
  setUnapprovedItemsCount: number
}

export interface Getters {
  waitingList: PatientVisitItem[]
}


export function state() {
  let state: State = {
    patientVisitItemList: [],
    patientVisitItemHistoryList: [],
    patientVisitItemHistoryPagination: {
      page: 1,
      page_size: 20
    },
    unapprovedItemsCount: null
  }
  return state
}

export const getters: DefineGetters<Getters, State> = {
  waitingList: state => state.patientVisitItemList.filter(f => f.approved === null || f.approved === undefined)
}

export const actions: DefineActions<Actions, State, Mutations, Getters> = {

  async createPatientVisitItem({commit}, reim) {
    await PatientVisitItemsService.patientVisitItemsCreate({
      data: reim
    })
  },

  async getPatientVisitItemList({commit, rootState}) {
    await PatientVisitItemsService.patientVisitItemsList({
      studyId: rootState.studies.study.id
    }).then(res => commit('setPatientVisitItemList', res.results))
  },

  async getPatientVisitItemHistoryList({commit, rootState}, filterObject) {
    await PatientVisitItemsService.patientVisitItemsList({
      page: rootState.patientvisititems.patientVisitItemHistoryPagination.page,
      pageSize: rootState.patientvisititems.patientVisitItemHistoryPagination.page_size,
      studyId: rootState.studies.study.id,
      ...filterObject
    }).then(res => commit('setPatientVisitItemHistoryList', res))
  },

  async getUnapprovedItemsCount({commit, rootState}) {
    await PatientVisitItemsService.patientVisitItemsList({
      approved: 'none',
      studyId: rootState.studies.study.id
    }).then(res => commit('setUnapprovedItemsCount', res.results.length))
  },

  async patchApproval({commit, rootState}, patchObj) {
    await PatientVisitItemsService.patientVisitItemsPartialUpdate({
      data: patchObj,
      id: patchObj.id
    })
  },

  async returnReimsForPatientVisit({commit}, patientVisitId) {
    return await PatientVisitItemsService.patientVisitItemsList({
      pageSize: 999,
      patientVisit: patientVisitId,
    })
  },
}

export const mutations: DefineMutations<Mutations, State> = {

  setPatientVisitItemList(state, patientVisitItemList) {
    state.patientVisitItemList = patientVisitItemList
  },

  setPatientVisitItemHistoryList(state, responseData) {
    state.patientVisitItemHistoryList = responseData.results
    state.patientVisitItemHistoryPagination = responseData.pagination
  },

  setPatientVisitItemHistoryPaginationPage(state, pageNumber) {
    state.patientVisitItemHistoryPagination.page = pageNumber
  },

  setPatientVisitItemHistoryPaginationSize(state, pageSize) {
    state.patientVisitItemHistoryPagination.page_size = pageSize
  },

  setUnapprovedItemsCount(state, count) {
    state.unapprovedItemsCount = count
  }
}

export const {
  mapState,
  mapGetters,
  mapMutations,
  mapActions,
} = createNamespacedHelpers<State, Getters, Mutations, Actions>('patientvisititems')

export const patientvisititems = {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
}
