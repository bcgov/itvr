import { useEffect, useRef } from 'react';
import axios from 'axios';
// axios.defaults.withCredentials = true;

import { useKeycloak } from '@react-keycloak/web';

const baseURL = process.env.REACT_APP_API_BASE;

const useAxios = (opts = {baseURL}) => {
  const axiosInstance = useRef();
  const { keycloak, initialized } = useKeycloak();
  const kcToken = keycloak?.token ?? '';

  useEffect(() => {
    axiosInstance.current = axios.create({
      ...opts,
      headers: {
        Authorization: initialized ? `Bearer ${kcToken}` : undefined,
      },
    });

    return () => {
      axiosInstance.current = undefined;
    };
  }, [opts, initialized, kcToken]);

  return axiosInstance;
};

export default useAxios;
