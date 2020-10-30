import { HttpError } from 'react-admin';
import {
  setCookie,
  getCookie,
  destroyCookie,
  request,
} from './utils';

export default {
  login: ({ username, password }) => {
    const identifier = username;
    const data = {
      identifier,
      password,
    };
    return request('post', '/users/refresh-tokens', data)
      .then((resp) => {
        const refreshToken = resp.data.refresh_token;
        const accessToken = resp.data.access_token;
        setCookie('refresh_token', refreshToken);
        setCookie('access_token', accessToken);
        setCookie('username', data.identifier);
      });
  },
  logout: () => {
    destroyCookie('refresh_token');
    destroyCookie('access_token');
    return Promise.resolve();
  },
  checkAuth: () => {
    const token = getCookie('access_token');
    return token ? Promise.resolve() : Promise.reject(new HttpError('Вы неавторизованы'));
  },
  checkError: (params) => {
    const { status } = params;
    if (status === 401 || status === 403) {
      localStorage.removeItem('token');
      localStorage.removeItem('role');
      return Promise.reject();
    }
    return Promise.resolve();
  },
  getPermissions: () => {
    const role = 'admin';
    return role ? Promise.resolve(role) : Promise.reject();
  },
  getIdentity: () => {
    const fullName = getCookie('username');
    const id = 1;
    const avatar = 'https://yt3.ggpht.com/a/AATXAJwH1h8IT5kqsbQ5IeySczyEOvVa9CPB7SJDEGMoHQ=s900-c-k-c0x00ffffff-no-rj';
    return { id, fullName, avatar };
  },
};
