import { createNamespacedHelpers } from 'vuex';
import { DefineActions, DefineGetters, DefineMutations } from 'vuex-type-helper';

export interface State {
  errorObject: {}
}

export interface Actions {}

export interface Mutations {
  clearErrorObject: void
  setErrorObject: Object
}

export interface Getters {}


export function state() {
  let state: State = {
    errorObject: {}
  };
  return state;
}

export const getters: DefineGetters<Getters, State> = {};

export const actions: DefineActions<Actions, State, Mutations, Getters> = {};

export const mutations: DefineMutations<Mutations, State> = {

  clearErrorObject(state) {
    state.errorObject = {}
  },

  setErrorObject(state, errorObject: Object) {
    state.errorObject = errorObject
  },
};

export const {
  mapState,
  mapGetters,
  mapMutations,
  mapActions,
} = createNamespacedHelpers<State, Getters, Mutations, Actions>('errors');

export const cars = {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};
