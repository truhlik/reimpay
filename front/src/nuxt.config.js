require('dotenv').config();

import localeSettings from './utils/localeSettings.js'

export default {
  mode: 'spa',
  /*
  ** Headers of the page
  */
  head: {
    title: 'Reimpay admin',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: process.env.npm_package_description || '' },
      { hid: 'author', name: 'author', content: 'Endevel s. r. o.' },
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/images/favicon.png' },
      { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css?family=Roboto:300,400,500,700|Material+Icons' }
    ],
    script: [
      {
        src: 'https://maps.googleapis.com/maps/api/js?key=AIzaSyAxOVlyMJ15IF8uFUUq_zZM6Hn7gvPi5j8&libraries=places'
      }
    ]
  },
  /*
  ** Customize the progress-bar color
  */
  loading: { color: '#fff' },
  /*
  ** Global CSS
  */
  css: [
    'assets/base.scss',
    'assets/variables.scss',
  ],
  /*
  ** Plugins to load before mounting the App
  */
  plugins: [
    { src: '~plugins/api.js' },
    { src: '~plugins/filters.js' },
    { src: '~plugins/i18n.js' },
    { src: '~plugins/places.js' }
  ],

  buildModules: [
    '@nuxt/typescript-build',
    '@nuxtjs/google-analytics'
  ],

  modules: [
    'nuxt-rfg-icon',
    '@nuxtjs/axios',
    '@nuxtjs/auth',
    '@nuxtjs/dotenv',
    '@nuxtjs/manifest',
    '@nuxtjs/sentry',
    '@nuxtjs/svg',
    '@nuxtjs/toast',
    '@nuxtjs/vuetify',
    'nuxt-i18n',
  ],

  auth: {
    redirect: {
      callback: '/auth/callback/',
      login: '/auth/login/',
      logout: '/auth/logout/'
    },
    strategies: {
      local: {
        endpoints: {
          login: { url: `${process.env.API_URL}/accounts/login/`, method: 'POST', propertyName: 'key' },
          logout: { url: `${process.env.API_URL}/accounts/logout/`, method: 'POST'},
          user: false // FIXME not working { url: `${process.env.API_URL}/accounts/user/`, method: 'GET'},
        },
        tokenRequired: true,
        tokenType: 'Token'
      },
    }
  },

  dotenv: {
    filename: '.env',
    systemvars: true
  },

  env: {
    API_URL: process.env.API_URL,
    GOOGLE_ANALYTICS_ID: process.env.GOOGLE_ANALYTICS_ID
  },

  googleAnalytics: {
    id: process.env.GOOGLE_ANALYTICS_ID || 'UA-175551193-1'
  },

  i18n: localeSettings,

  router: {
    base: '/app/',
    middleware: ['auth'],
    mode: 'hash',
    trailingSlash: true
  },

  sentry: {
    dsn: process.env.SENTRY_DSN || '',
  },

  toast: {
    duration: 4000,
    position: 'top-center',
  },

  vuetify: {
    breakpoint: {
      // thresholds: {
      //   xs: 0,
      //   sm: 600,
      //   md: 960,
      //   lg: 1280,
      //   xl: 1950
      // },
    },
    customVariables: ['~/assets/variables.scss'],
    theme: {
      themes: {
        light: {
          primary: '#36A693',
          // accent: colors.grey.darken3,
          // secondary: colors.amber.darken3,
          // info: colors.teal.lighten1,
          warning: '#ffc519',
          error: '#e55b64',
          success: '#06d6a0'
        }
      }
    },
    treeShake: true
  },

  /*
  ** Build configuration
  */
  build: {
    /*
    ** You can extend webpack config here
    */
    extend(config, ctx) {
      if (ctx.isDev) {
        // magic for debugging purposes
        // https://medium.com/js-dojo/debugging-nuxt-js-with-vs-code-60a1a9e75cf6
        config.devtool = ctx.isClient ? 'source-map' : 'inline-source-map'
      }
    }
  },
}
