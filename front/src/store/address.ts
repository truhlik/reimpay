import { createNamespacedHelpers } from 'vuex'
import { DefineActions, DefineGetters, DefineMutations } from 'vuex-type-helper'

import { getOptionString } from '~/helpers/addressHelpers'
import {
  AddressesService, AddressSuggestion
} from "~/service/api"

export interface State {
  // city: string
  // cityOptions: Object[]
  street: string
  streetOptions: Object[]
  // zip: string
  // zipOptions: Object[]

  // loadingCity: Boolean
  loadingStreet: Boolean
  // loadingZip: Boolean
}

export interface Actions {
  getSuggestion: string
}

export interface Mutations {
  setLoading: Boolean
  setSuggestionOptions: AddressSuggestion[]
  updateAddressField: {field: string, value: string}
}

export interface Getters {
  // isAdmin: Boolean
}


export function state() {
  let state: State = {
    // city: '',
    // cityOptions: [],
    street: '',
    streetOptions: [],
    // zip: '',
    // zipOptions: [],

    // loadingCity: false,
    loadingStreet: false,
    // loadingZip: false
  }
  return state
}

export const getters: DefineGetters<Getters, State> = {
  // isAdmin: state => (state.user as any).role === 'ADMIN'
}

export const actions: DefineActions<Actions, State, Mutations, Getters> = {

  async getSuggestion({commit, rootState}, value) {
    commit('setLoading', true)

    await AddressesService.addressesSuggestionCreate({
      data: {
        city: '', // rootState.address.city ? rootState.address.city : '',
        number: '',
        post_code: '', // rootState.address.zip ? rootState.address.zip : '',
        street: value, // rootState.address.street ? rootState.address.street : '',
        suggesting_field: '' // field
      }
    })
      .then(res => commit('setSuggestionOptions', res.results)
    )

    commit('setLoading', false)
  },
}

export const mutations: DefineMutations<Mutations, State> = {

  setLoading(state, isLoading){
    // state.loadingCity = isLoading
    state.loadingStreet = isLoading
    // state.loadingZip = isLoading
  },

  setSuggestionOptions(state, suggestionList) {
    // state.streetOptions = suggestionList.map(s => ({value: s, text: `${s.street}, ${s.city}`}))
    state.streetOptions = suggestionList
      .filter(sug => !!sug.street && !!sug.number)
      .map(sug => ({
        value: sug,
        text: getOptionString(sug)
      }))
    // state.cityOptions = suggestionList.filter(s => !!s.city).map(s => ({value: s, text: s.city}))
    // state.zipOptions = suggestionList.filter(s => !!s.post_code).map(s => ({value: s, text: s.post_code}))
  },

  updateAddressField(state, {field, value}) {
    (state as any)[field] = value
  }
}

export const {
  mapState,
  mapGetters,
  mapMutations,
  mapActions,
} = createNamespacedHelpers<State, Getters, Mutations, Actions>('address')

export const address = {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
}
