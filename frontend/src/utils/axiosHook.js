import { useEffect, useRef } from 'react';
import axios from 'axios';
import { useDominantKeycloak } from '../keycloak';

const baseURL = process.env.REACT_APP_API_BASE;

const useAxios = (opts = {}) => {
  const axiosInstance = useRef();
  const keycloak = useDominantKeycloak();

  useEffect(() => {
    const instance = axios.create({
      baseURL,
      ...opts,
      headers: {}
    });
    instance.interceptors.request.use((config) => {
      if (keycloak) {
        return keycloak.updateToken().then(() => {
          config.headers.Authorization = `Bearer ${keycloak.token}`;
          return config;
        });
      }
      return config;
    });
    axiosInstance.current = instance;

    return () => {
      axiosInstance.current = undefined;
    };
  }, [opts, keycloak]);

  return axiosInstance;
};

export default useAxios;
