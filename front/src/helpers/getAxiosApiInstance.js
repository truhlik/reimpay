import axios from 'axios';
import Cookies from 'js-cookie';

export default function getAxiosApiInstance() {

  const instance = axios.create({
    baseURL: process.env.API_URL,
    headers: {
      'Content-Language': localStorage.getItem('lang') || navigator.language
    }
  });

  instance.defaults.headers.common['Authorization'] = `${Cookies.get('auth._token.social')}`;

  instance.interceptors.response.use(
    response => response,
    error => console.error(error)   // TODO rise toast.alert
  );

  return instance;
}
