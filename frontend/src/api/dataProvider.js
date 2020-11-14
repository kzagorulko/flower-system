/* eslint-disable no-console */
import {
  request,
  prepareImage,
} from './utils';

const flatParams = (params) => {
  let result = {};
  Object.entries(params).forEach(
    (e) => { result = e[1] instanceof Object ? { ...e[1], ...result } : { ...e, ...result }; },
  );
  return result;
};

export default {
  getList: (resource, params) => request('GET', `/${resource}/`, flatParams(params))
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

  create: (resource, params) => prepareImage(params)
    .then((preparedParams) => request('POST', `/${resource}/`, preparedParams.data)
      .then((resp) => {
        const { data } = resp;
        return {
          data,
        };
      })),

  // TODO: fix
  update: (resource, params) => prepareImage(params)
    .then((preparedParams) => request('PATCH', `/${resource}/${preparedParams.id}`, preparedParams.data)
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
};
