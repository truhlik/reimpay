import { createNamespacedHelpers } from 'vuex'
import { DefineActions, DefineGetters, DefineMutations } from 'vuex-type-helper'

import {
  PatientsService, PatientBase, PatientDetail, EnumPatientBasePaymentType
} from '~/service/api'


export interface State {
  activePatientCount: number | null
  patient: PatientBase
  patientDetail: PatientDetail | null
  patientList: PatientBase[]
  toEditList: PatientBase[]
}

export interface Actions {
  createPatient: void
  getPatient: number
  getActivePatientCount: void
  getPatientList: number
  getToEditList: void
  partialUpdatePatient: PatientBase
  updatePatient: void
}

export interface Mutations {
  clearPatient: void
  setActivePatientCount: number
  setPatient: PatientBase
  setPatientDetail: PatientDetail
  setPatientList: PatientBase[]
  setToEditList: PatientBase[]
  updatePatientField: {field: string, value: string}
}

export interface Getters {
  patientOptionList: Object[]
  paymentInfoOptionList: Object[]
}


export function state() {
  let state: State = {
    activePatientCount: null,
    patient: new PatientBase({payment_type: EnumPatientBasePaymentType['BANK']}),
    patientDetail: null,
    patientList: [],
    toEditList: []
  }
  return state
}

export const getters: DefineGetters<Getters, State> = {
  patientOptionList: state => state.patientList.map(p => ({value: p.id, text: p.number})),
  paymentInfoOptionList: () => (Object.keys(EnumPatientBasePaymentType).map(pt => ({value: pt, text: pt})))
}

export const actions: DefineActions<Actions, State, Mutations, Getters> = {

  async createPatient({commit, rootState}) {
    await PatientsService.patientsCreate({
      data: rootState.patients.patient
    }).then(res => commit('setPatient', res))
  },

  async getPatient({commit}, patientId: number) {
    await PatientsService.patientsRead({
      id: patientId
    }).then(res => commit('setPatientDetail', res)
    )
  },

  async getPatientList({commit, rootState}, siteId?) {
    await PatientsService.patientsList({
      studyId: rootState.studies.study.id || '',
      siteId: siteId,
      pageSize: 9999
    }).then(res => commit('setPatientList', res.results)
    )
  },

  async getActivePatientCount({commit, rootState}) {
    await PatientsService.patientsList({
      studyId: rootState.studies.study.id || '',
      active: 'true'
    }).then(res => commit('setActivePatientCount', res.results.length)
    )
  },

  async partialUpdatePatient({commit, rootState}, patchData) {
    await PatientsService.patientsPartialUpdate({
      data: patchData,
      id: patchData.id
    })
  },

  async getToEditList({commit, rootState}) {
    await PatientsService.patientsList({
      changePayment: 'true',
      studyId: rootState.studies.study.id || '',
      pageSize: 9999
    }).then(res => commit('setToEditList', res.results)
    )
  },

  async updatePatient({commit, rootState}) {
    await PatientsService.patientsUpdate({
      data: rootState.patients.patient,
      id: rootState.patients.patient.id
    }).then(res => commit('setPatient', res))
  },
}

export const mutations: DefineMutations<Mutations, State> = {

  clearPatient(state) {
    state.patient = new PatientBase({payment_type: EnumPatientBasePaymentType['BANK']})
  },

  setActivePatientCount(state, count: number) {
    state.activePatientCount = count
  },

  setPatient(state, patient: PatientBase) {
    state.patient = patient
  },

  setPatientDetail(state, patient: PatientDetail) {
    state.patientDetail = patient
  },

  setPatientList(state, patientList) {
    state.patientList = patientList
  },

  setToEditList(state, patientList) {
    state.toEditList = patientList
  },

  updatePatientField(state, {field: field, value: value}) {
    (state.patient as any)[field] = value
  },
}

export const {
  mapState,
  mapGetters,
  mapMutations,
  mapActions,
} = createNamespacedHelpers<State, Getters, Mutations, Actions>('patients')

export const patients = {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
}
