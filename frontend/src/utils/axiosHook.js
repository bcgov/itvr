import { useEffect, useRef } from 'react';
import axios from 'axios';
// import settings from './settings';
// const { API_BASE } = settings;
// axios.defaults.withCredentials = true;
// axios.defaults.baseURL = API_BASE;

import { useKeycloak } from '@react-keycloak/web';

const useAxios = (baseURL) => {
  const axiosInstance = useRef();
  const { keycloak, initialized } = useKeycloak();
  const kcToken = keycloak?.token ?? '';

  useEffect(() => {
    axiosInstance.current = axios.create({
      baseURL,
      headers: {
        Authorization: initialized ? `Bearer ${kcToken}` : undefined,
      },
    });

    return () => {
      axiosInstance.current = undefined;
    };
  }, [baseURL, initialized, kcToken]);

  return axiosInstance;
};

export default useAxios;
