import { createNamespacedHelpers } from 'vuex';
import { DefineActions, DefineGetters, DefineMutations } from 'vuex-type-helper';

import {
  ArmsService, Arm
} from '~/service/api';


export interface State {
  arm: Arm | Object,
  armList: Arm[],
}

export interface Actions {
  createArm: void
  deleteArm: number
  getArm: number
  getArmList: void
  updateArm: void
}

export interface Mutations {
  clearArm: void
  setArm: Arm
  setArmList: Arm[]
  updateArmField: {field: string, value: string}
}

export interface Getters {
  armOptionList: Object[]
}


export function state() {
  let state: State = {
    arm: {},
    armList: []
  };
  return state;
}

export const getters: DefineGetters<Getters, State> = {
  armOptionList: state => state.armList.map(a => ({value: a.id, text: a.title}))
};

export const actions: DefineActions<Actions, State, Mutations, Getters> = {

  async createArm({commit, rootState}) {
    await ArmsService.armsCreate({
      data: {
        ...rootState.arms.arm,
        study: rootState.studies.study.id
      }
    }).then(res => commit('setArm', res));
  },

  async deleteArm({commit, rootState}, armId: number) {
    await ArmsService.armsDelete({
      id: armId
    });
  },

  async getArm({commit}, armId: number) {
    await ArmsService.armsRead({
      id: armId
    }).then(res => commit('setArm', res)
    );
  },

  async getArmList({commit, rootState}) {
    await ArmsService.armsList({
      studyId: rootState.studies.study.id || ''
    }).then(res => commit('setArmList', res.results)
    );
  },

  async updateArm({commit, rootState}) {
    await ArmsService.armsUpdate({
      data: {...rootState.arms.arm},
      id: rootState.arms.arm.id
    }).then(res => commit('setArm', res));
  },
};

export const mutations: DefineMutations<Mutations, State> = {

  clearArm(state) {
    state.arm = {};
  },

  setArm(state, arm: Arm) {
    state.arm = arm;
  },

  setArmList(state, userList) {
    state.armList = userList;
  },

  updateArmField(state, {field: field, value: value}) {
    (state.arm as any)[field] = value;
  },
};

export const {
  mapState,
  mapGetters,
  mapMutations,
  mapActions,
} = createNamespacedHelpers<State, Getters, Mutations, Actions>('arms');

export const arms = {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};
