import { createNamespacedHelpers } from 'vuex'
import { DefineActions, DefineGetters, DefineMutations } from 'vuex-type-helper'

import {
  PatientVisitsService, PatientVisit
} from '~/service/api'

export interface State {
  patientVisitList: PatientVisit[]
}

export interface Actions {
  createPatientVisit: PatientVisit
  deletePatientVisit: number
  getPatientVisitList: string
}

export interface Mutations {
  setPatientVisitList: PatientVisit[]
}

export interface Getters {
  patientVisitOptionList: Object[]
}

export function state() {
  let state: State
  state = {
    patientVisitList: []
  }
  return state
}

export const getters: DefineGetters<Getters, State> = {
  patientVisitOptionList: state => state.patientVisitList.map(pv => ({value: pv, text: pv.title})),
}

export const actions: DefineActions<Actions, State, Mutations, Getters> = {

  async createPatientVisit({commit}, visitData) {
    await PatientVisitsService.patientVisitsCreate({
      data: visitData
    })
  },

  async deletePatientVisit({commit}, patientVisitId) {
    await PatientVisitsService.patientVisitsDelete({
      id: patientVisitId
    })
  },

  async getPatientVisitList({commit}, patientId) {
    await PatientVisitsService.patientVisitsList({
      patientId: patientId
    }).then((res) => commit('setPatientVisitList', res.results))
  }
}

export const mutations: DefineMutations<Mutations, State> = {
  setPatientVisitList(state, patientVisitList) {
    state.patientVisitList = patientVisitList
  }
}

export const {
  mapState,
  mapGetters,
  mapMutations,
  mapActions,
} = createNamespacedHelpers<State, Getters, Mutations, Actions>('patientvisits')

export const patientvisits = {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
}
