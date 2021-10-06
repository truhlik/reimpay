import { createNamespacedHelpers } from 'vuex'
import { DefineActions, DefineGetters, DefineMutations } from 'vuex-type-helper'

import {
  BaseCompany, CompaniesService, EnumUserRole, User, StudiesService, UsersService
} from "~/service/api"

export interface State {
  company: BaseCompany | Object
  studyCraList: User[]
  userList: User[]
}

export interface Actions {
  createUser: User
  deleteUser: string

  getCompanyForUser: void
  // getStudyCraList: void
  getUserList: void
}

export interface Mutations {
  setCompany: BaseCompany
  setStudyCraList: User[]
  setUserList: User[]
  updateCompanyField: {field: string, value: string}
}

export interface Getters {
  // studyCraOptions: Object[]
  userAdminList: User[]
  userCraList: User[]
  userCraIdOptions: Object[]
  userCraOptions: Object[]
}


export function state() {
  let state: State = {
    company: {},
    studyCraList: [],
    userList: []
  }
  return state
}

export const getters: DefineGetters<Getters, State> = {
  // studyCraOptions: (state: State) => state.studyCraList.map(u => ({value: u.id, text: `${u.first_name} ${u.last_name}`})),
  userAdminList: (state: State) => state.userList.filter(u => u.role === EnumUserRole['ADMIN']),
  userCraList: (state: State) => state.userList.filter(u => u.role === EnumUserRole['CRA']),
  userCraIdOptions: (state: State) => state.userList.filter(u => u.role === EnumUserRole['CRA'])
                                                  .map(u => ({value: u.id, text: `${u.first_name} ${u.last_name}`})),
  userCraOptions: (state: State) => state.userList.filter(u => u.role === EnumUserRole['CRA'])    // FIXME the value is strange
                                                  .map(u => ({value: {id: u.id}, text: `${u.first_name} ${u.last_name}`})),
}

export const actions: DefineActions<Actions, State, Mutations, Getters> = {

  async createUser({commit}, user: User) {
    await UsersService.usersCreate({
      data: user
    })
  },

  async deleteUser({commit}, userId: string) {
    await UsersService.usersDelete({
      id: userId
    })
  },

  async getCompanyForUser({commit}) {
    await CompaniesService.companiesPrimaryRead(
    ).then(res => commit('setCompany', res))
  },

  // async getStudyCraList({commit, rootState}) {
  //   await UsersService.usersList({
  //     pageSize: 999,
  //     role: 'CRA',
  //     studyId: rootState.studies.study.id
  //   }).then(res => commit('setStudyCraList', res.results))
  // },

  async getUserList({commit}) {
    await UsersService.usersList().then(res => commit('setUserList', res.results))
  },
}

export const mutations: DefineMutations<Mutations, State> = {

  setCompany(state, company: BaseCompany) {
    state.company = company
  },

  setStudyCraList(state, userList) {
    state.studyCraList = userList
  },

  setUserList(state, userList) {
    state.userList = userList
  },

  updateCompanyField(state, {field: field, value: value}) {
    (state.company as any)[field] = value
  },
}

export const {
  mapState,
  mapGetters,
  mapMutations,
  mapActions,
} = createNamespacedHelpers<State, Getters, Mutations, Actions>('company')

export const company = {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
}
