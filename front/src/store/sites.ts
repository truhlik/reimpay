import { createNamespacedHelpers } from 'vuex'
import { DefineActions, DefineGetters, DefineMutations } from 'vuex-type-helper'

import {
  SitesService, Site, SitePatient
} from '~/service/api'


export interface State {
  site: Site,
  siteList: Site[],
  sitePatientList: SitePatient[]
}

export interface Actions {
  createSite: void
  deleteSite: number
  getSite: number
  getSiteList: void
  getSitePatientList: void
  updateSite: void
}

export interface Mutations {
  clearSite: void
  setSite: Site
  setSiteList: Site[]
  setSitePatientList: SitePatient[]
  updateSiteField: {field: string, value: string}
}

export interface Getters {
  siteOptionList: Object[]
}


export function state() {
  let state: State = {
    site: new Site(),
    siteList: [],
    sitePatientList: []
  }
  return state
}

export const getters: DefineGetters<Getters, State> = {
  siteOptionList: state => state.siteList.map(s => ({value: s.id, text: s.title}))
}

export const actions: DefineActions<Actions, State, Mutations, Getters> = {

  async createSite({commit, rootState}) {
    await SitesService.sitesCreate({
      data: {
        ...rootState.sites.site,
        study: rootState.studies.study.id
      }
    }).then(res => commit('setSite', res))
  },

  async deleteSite({commit, rootState}, siteId: number) {
    await SitesService.sitesDelete({
      id: siteId
    })
  },

  async getSite({commit}, siteId: number) {
    await SitesService.sitesRead({
      id: siteId
    }).then(res => commit('setSite', res)
    )
  },

  async getSiteList({commit, rootState}) {
    await SitesService.sitesList({
      studyId: rootState.studies.study.id || ''
    }).then(res => commit('setSiteList', res.results)
    )
  },

  async getSitePatientList({commit, rootState}) {
    await SitesService.sitesPatients({
      studyId: rootState.studies.study.id || ''
    }).then(res => commit('setSitePatientList', res.results)
    )
  },

  async updateSite({commit, rootState}) {
    await SitesService.sitesUpdate({
      data: {...rootState.sites.site},
      id: rootState.sites.site.id
    }).then(res => commit('setSite', res))
  },
}

export const mutations: DefineMutations<Mutations, State> = {

  clearSite(state) {
    state.site = new Site()
  },

  setSite(state, site: Site) {
    state.site = site
  },

  setSiteList(state, siteList) {
    state.siteList = siteList
  },

  setSitePatientList(state, sitePatientList) {
    state.sitePatientList = sitePatientList
  },

  updateSiteField(state, {field: field, value: value}) {
    (state.site as any)[field] = value
  },
}

export const {
  mapState,
  mapGetters,
  mapMutations,
  mapActions,
} = createNamespacedHelpers<State, Getters, Mutations, Actions>('sites')

export const sites = {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
}
