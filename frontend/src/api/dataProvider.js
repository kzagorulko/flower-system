/* eslint-disable no-console */
import {
  request,
} from './utils';

export default {
  getList: (resource, params) => {
    // params not implemented: filters, pagination etc
    console.log(params);
    return request('GET', `/${resource}/`)
      .then((resp) => {
        const { total } = resp.data;
        return {
          data: resp.data.items.map((value) => ({
            id: value.id,
            ...value,
          })),
          total,
        };
      });
  },

  getOne: (resource, params) => {
    console.log(params);
    return request('GET', `/${resource}/${params.id}`)
      .then((resp) => {
        const { data } = resp;
        return {
          data,
        };
      });
  },

  getMany: () => {},

  getManyReference: () => {},

  create: (resource, params) => request('POST', `/${resource}/`, params.data)
    .then((resp) => {
      const { data } = resp;
      return {
        data,
      };
    }),

  update: (resource, params) => request('PATCH', `/${resource}/${params.id}`, params.data)
    .then(() => {
      const data = {
        id: params.id,
      };
      return {
        data,
      };
    }),

  updateMany: () => {},

  delete: () => {},

  deleteMany: () => {},
};
