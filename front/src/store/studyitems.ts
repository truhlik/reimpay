import { createNamespacedHelpers } from 'vuex';
import { DefineActions, DefineGetters, DefineMutations } from 'vuex-type-helper';

import {
  StudyItemsService, StudyItem
} from '~/service/api';


export interface State {
  studyItem: StudyItem | Object,
  studyItemList: StudyItem[],
}

export interface Actions {
  createStudyItem: StudyItem
  deleteStudyItem: number
  getStudyItem: number
  getStudyItemList: void
  updateStudyItem: void
}

export interface Mutations {
  clearStudyItem: void
  setStudyItem: StudyItem
  setStudyItemList: StudyItem[]
  updateStudyItemField: {field: string, value: string}
}

export interface Getters {
  studyItemOptionList: Object[]
}

export function state() {
  let state: State = {
    studyItem: {},
    studyItemList: []
  };
  return state;
}

export const getters: DefineGetters<Getters, State> = {
  studyItemOptionList: state => state.studyItemList.map(s => ({value: s.id, text: s.title}))
};

export const actions: DefineActions<Actions, State, Mutations, Getters> = {

  async createStudyItem({commit, rootState}, studyItem) {
    await StudyItemsService.studyItemsCreate({
      data: {
        ...studyItem
      }
    }).then(res => commit('setStudyItem', res));
  },

  async deleteStudyItem({commit, rootState}, studyItemId: number) {
    await StudyItemsService.studyItemsDelete({
      id: studyItemId
    });
  },

  async getStudyItem({commit}, studyItemId: number) {
    await StudyItemsService.studyItemsRead({
      id: studyItemId
    }).then(res => commit('setStudyItem', res)
    );
  },

  async getStudyItemList({commit, rootState}) {
    await StudyItemsService.studyItemsList({
      studyId: rootState.studies.study.id || ''
    }).then(res => commit('setStudyItemList', res.results)
    );
  },

  async updateStudyItem({commit, rootState}) {
    await StudyItemsService.studyItemsUpdate({
      data: {...rootState.studyitems.studyItem},
      id: rootState.studyitems.studyItem.id
    }).then(res => commit('setStudyItem', res));
  },
};

export const mutations: DefineMutations<Mutations, State> = {

  clearStudyItem(state) {
    state.studyItem = {};
  },

  setStudyItem(state, studyItem: StudyItem) {
    state.studyItem = studyItem;
  },

  setStudyItemList(state, userList) {
    state.studyItemList = userList;
  },

  updateStudyItemField(state, {field: field, value: value}) {
    (state.studyItem as any)[field] = value;
  },
};

export const {
  mapState,
  mapGetters,
  mapMutations,
  mapActions,
} = createNamespacedHelpers<State, Getters, Mutations, Actions>('studyItems');

export const studyItems = {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};
