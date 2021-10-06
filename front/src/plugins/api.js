import Cookies from 'js-cookie'
import handleErrorResponse from "~/helpers/handleErrorResponse";
import { serviceOptions } from "~/service/api";


export default function ({ $axios, redirect }) {
//   $axios.onRequest(config => {
//     // if (config.data && typeof(config.data) === "object") {
//     //   for (let key in config.data) {
//     //     if(config.data[key] === '') config.data[key] = null;
//     //   }
//     // }
//     return config;
//   }, function (error) {
//     return Promise.reject(error);
//   });

  $axios.onError(err => {
    if (!err.response) return Promise.reject(err);

    if (err.response.status === 401) {
      // Unauthorized -> remove token and redirect to login
      window.$nuxt.$auth.setToken('local', null);
      // window.$nuxt.$router.push(window.$nuxt.localePath({name: 'auth-login'}));
      location.href = '/app/#/auth/login/'
    } else {
      const handledError = handleErrorResponse(err.response);

      if (handledError.errorObject) window.$nuxt.$store.commit('errors/setErrorObject', handledError.errorObject);
      // if (handledError.message) window.$nuxt.$toasted.error(handledError.message);

      return Promise.reject(handledError);
    }
  });

  $axios.defaults.baseURL = process.env.API_URL;
  $axios.defaults.headers.common['Content-Language'] = localStorage.getItem('lang') || navigator.language;
  // $axios.defaults.headers.common['Authorization'] = Cookies.get('auth._token.local'); automatically by nuxt?

  serviceOptions.axios = $axios;
}
