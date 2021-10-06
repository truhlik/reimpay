import { createNamespacedHelpers } from 'vuex';
import { DefineActions, DefineGetters, DefineMutations } from 'vuex-type-helper';

import {
  StudiesService, StudyRead, StudyWrite
} from "~/service/api";


export interface State {
  study: StudyRead | StudyWrite
  studyList: StudyRead[]
}

export interface Actions {
  createStudy: void
  deleteStudy: string
  getStudy: string
  getStudyList: void
  patchStudy: object
  updateStudy: void
}

export interface Mutations {
  clearStudy: void
  setStudy: StudyRead | StudyWrite
  setStudyList: StudyRead[]
  updateStudyField: {field: string, value: string}
  updateStudyUsers: String[]
}

export interface Getters {}


export function state() {
  let state: State = {
    study: new StudyWrite({ pay_frequency: 1 }),
    studyList: []
  };
  return state;
}

export const getters: DefineGetters<Getters, State> = {};

export const actions: DefineActions<Actions, State, Mutations, Getters> = {

  async createStudy({commit, rootState}) {
    await StudiesService.studiesCreate({
      data: rootState.studies.study
    }).then(res => commit('setStudy', res));
  },

  async deleteStudy({commit, rootState}, studyId: string) {
    await StudiesService.studiesDelete({
      id: studyId
    })
  },

  async getStudy({commit}, studyId: string) {
    await StudiesService.studiesRead({
      id: studyId
    }).then(res => commit('setStudy', res)
    );
  },

  async getStudyList({commit}) {
    await StudiesService.studiesList(
    ).then(res => commit('setStudyList', res.results)
    );
  },

  async patchStudy({commit, rootState}, patchData) {
    await StudiesService.studiesPartialUpdate({
      data: new StudyWrite(patchData),
      id: rootState.studies.study.id
    }).then(res => commit('setStudy', res));
  },

  async updateStudy({commit, rootState}) {
    await StudiesService.studiesUpdate({
      data: rootState.studies.study,
      id: rootState.studies.study.id
    }).then(res => commit('setStudy', res));
  },
};

export const mutations: DefineMutations<Mutations, State> = {

  clearStudy(state) {
    state.study = new StudyWrite({ pay_frequency: 1 })
  },

  setStudy(state, study: StudyRead | StudyWrite) {
    state.study = study;
  },

  setStudyList(state, userList) {
    state.studyList = userList;
  },

  updateStudyField(state, {field: field, value: value}) {
    (state.study as any)[field] = value;
  },

  updateStudyUsers(state, userIdArray: String[]) {
    (state.study as any)['users'] = userIdArray
  },
};

export const {
  mapState,
  mapGetters,
  mapMutations,
  mapActions,
} = createNamespacedHelpers<State, Getters, Mutations, Actions>('studies');

export const studies = {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};
