import axios, { AxiosRequestTransformer, AxiosResponseTransformer } from 'axios';
import { camelizeKeys, decamelizeKeys } from 'humps';
import { API_HOST } from '@/constants/backend';

export const client = axios.create({
  baseURL: API_HOST,
  headers: {
    'Content-Type': 'application/json',
  },
  transformResponse: [
    ...(axios.defaults.transformResponse as AxiosResponseTransformer[]),
    (data) => camelizeKeys(data),
  ],
  transformRequest: [
    (data) => decamelizeKeys(data),
    ...(axios.defaults.transformRequest as AxiosRequestTransformer[]),
  ],
});

client.interceptors.request.use((config) => {
  const { params, ...noParamsConfig } = config;
  return { ...noParamsConfig, params: decamelizeKeys(params) };
});
