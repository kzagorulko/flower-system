import axios from 'axios';
import { HttpError } from 'react-admin';
import {
  AUTH_LOGIN,
} from './actions';

export default (apiUrl) => (type, params) => {
  let url = '';

  switch (type) {
  case AUTH_LOGIN: {
    const { username, password } = params;
    const identifier = username;
    const data = {
      identifier,
      password,
    };
    url = `${apiUrl}/users/refresh-tokens`;

    return axios.post(url, data)
      .then((resp) => {
        const refreshToken = resp.data.refresh_token;
        const accessToken = resp.data.access_token;
        localStorage.setItem('refresh_token', refreshToken);
        localStorage.setItem('access_token', accessToken);
        return Promise.resolve();
      })
      .catch((err) => {
        if (err.response) {
          return Promise.reject(new HttpError(err.response.data.description));
        }
        if (err.request) {
          return Promise.reject(new HttpError(err.request.statusText));
        }
        return Promise.reject(new HttpError(err));
      });
  }
  default: {
    return Promise.reject();
  }
  }
};
