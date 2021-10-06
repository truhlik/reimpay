import { createNamespacedHelpers } from 'vuex'
import { DefineActions, DefineGetters, DefineMutations } from 'vuex-type-helper'

import {
  StudyConfig, StudiesService
} from "~/service/api"

import { SelectOptionList } from '~/types/general'

export interface State {
  config: Object | null
}

export interface Actions {
  getStudyConfig: void
}

export interface Mutations {
  setConfig: StudyConfig
}

export interface Getters {}


export function state() {
  let state: State = {
    config: null
  }
  return state
}

export const getters: DefineGetters<Getters, State> = {}

export const actions: DefineActions<Actions, State, Mutations, Getters> = {

  async getStudyConfig({commit, rootState}) {
    await StudiesService.studiesConfig({
      id: rootState.studies.study.id || null
    }).then(res => commit('setConfig', res))
  },
}

export const mutations: DefineMutations<Mutations, State> = {

  setConfig(state, studyConfig: StudyConfig) {
    state.config = studyConfig.config
  },
}

export const {
  mapState,
  mapGetters,
  mapMutations,
  mapActions,
} = createNamespacedHelpers<State, Getters, Mutations, Actions>('studyconfig')

export const studyconfig = {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
}
