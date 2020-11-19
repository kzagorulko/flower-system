/* eslint-disable no-console */
import {
  request,
  prepareImage,
  prepareUrl,
} from './utils';

const flatParams = (params) => {
  let result = {};
  if (!params) {
    return params;
  }
  Object.entries(params).forEach(
    (e) => { result = e[1] instanceof Object ? { ...e[1], ...result } : { ...e, ...result }; },
  );
  return result;
};

export default {
  getList: (resource, params) => request('GET', prepareUrl(`/${resource}/`), flatParams(params))
    .then((resp) => {
      const { total } = resp.data;
      return {
        data: resp.data.items.map((value) => ({
          id: value.id,
          ...value,
        })),
        total,
      };
    }),

  getOne: (resource, params) => {
    console.log(params);
    return request('GET', prepareUrl(`/${resource}/${params.id}`))
      .then((resp) => {
        const { data } = resp;
        return {
          data,
        };
      });
  },

  getMany: () => {},

  getManyReference: () => {},

  create: (resource, params) => prepareImage(params)
    .then((preparedParams) => request('POST', prepareUrl(`/${resource}/`), preparedParams.data)
      .then((resp) => {
        const { data } = resp;
        return {
          data,
        };
      })),

  update: (resource, params) => prepareImage(params)
    .then((preparedParams) => request('PATCH', prepareUrl(`/${resource}/${preparedParams.id}`), preparedParams.data)
      .then(() => {
        const data = {
          id: preparedParams.id,
        };
        return {
          data,
        };
      })),

  updateMany: () => {},

  delete: () => {},

  deleteMany: () => {},

  getCategories: (resource) => request('GET', `/${resource}/categories`)
    .then((resp) => resp.data.categories),

  updateStatus: (resource, params) => request('PATCH', `/${resource}/${params.id}/status`, params),
};
