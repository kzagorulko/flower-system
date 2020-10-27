import axios from 'axios';
import { HttpError } from 'react-admin';
import {
  GET_LIST,
  GET_ONE,
  CREATE,
  UPDATE,
} from './actions';

export default (
  apiUrl,
) => (type, resource, params) => {
  let url = '';

  // not implemented yet: pagination, filter
  console.log(params);

  // axios options for headers etc
  const options = {};

  switch (type) {
  case GET_LIST: {
    url = `${apiUrl}/${resource}/`;
    break;
  }

  case GET_ONE: {
    url = `${apiUrl}/${resource}/${params.id}`;
    break;
  }

  case CREATE: {
    url = `${apiUrl}/${resource}/`;
    options.method = 'POST';
    const { data } = params;
    options.data = data;
    break;
  }

  case UPDATE: {
    url = `${apiUrl}/${resource}/${params.id}`;

    const attributes = params.data;
    delete attributes.id;

    const { data } = params;
    options.method = 'PATCH';
    options.data = data;
    break;
  }

  default:
    return Promise.reject(new HttpError(`${type} not implemented yet`));
  }

  return axios({ url, ...options })
    .then((resp) => {
      const { total } = resp.data;

      switch (type) {
      case GET_LIST: {
        return {
          data: resp.data.items.map((value) => ({
            id: value.id,
            ...value,
          })),
          total,
        };
      }

      case GET_ONE: {
        const { data } = resp;
        return {
          data,
        };
      }

      case CREATE: {
        const { data } = resp;
        return {
          data,
        };
      }

      case UPDATE: {
        const data = {
          id: params.id,
        };
        return {
          data,
        };
      }

      default:
        return Promise.reject(new HttpError(`${type} not implemented yet`));
      }
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
};
